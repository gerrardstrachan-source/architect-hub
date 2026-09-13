#!/usr/bin/env python3
import csv, glob, pathlib, statistics, json, math, re

ACC_TOL = 0.05
TTC_TOL = 20
RT_LOW, RT_HIGH = 0.90, 1.10
PAIR_PASS_RATE = 0.90
EXPECTED_HEADER = ['trial','history','c','x','y','production','action','correct_action','correctness','feedback','rt','rng_state']
EXPECTED_FIXTURE = 'H2-W0.3-TRAINING-ONLY.csv'


def load_metadata(path, expected_history, expected_seed):
    meta_path = pathlib.Path(str(path) + '.metadata.txt')
    if not meta_path.exists():
        raise ValueError(f'{path}: missing runtime metadata sidecar')
    meta = {}
    for line in meta_path.read_text().splitlines():
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        meta[k.strip()] = v.strip()
    if meta.get('history') != expected_history:
        raise ValueError(f'{path}: metadata history mismatch')
    try:
        meta_seed = int(meta.get('seed', ''))
    except ValueError:
        raise ValueError(f'{path}: metadata seed is not an integer')
    if meta_seed != expected_seed:
        raise ValueError(f'{path}: metadata seed mismatch')
    if meta.get('seed-offset') != '0':
        raise ValueError(f'{path}: metadata seed offset mismatch')
    if meta.get('fixture') != EXPECTED_FIXTURE:
        raise ValueError(f'{path}: metadata fixture mismatch')
    if not meta.get('parameter-state'):
        raise ValueError(f'{path}: missing parameter-state metadata')
    if not meta.get('initial-rng-state'):
        raise ValueError(f'{path}: missing initial-rng-state metadata')


def load_run(path, expected_history, expected_seed):
    load_metadata(path, expected_history, expected_seed)
    with open(path, newline='') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != EXPECTED_HEADER:
            raise ValueError(f'{path}: header mismatch')
        rows = list(reader)
    if len(rows) != 192:
        raise ValueError(f'{path}: expected 192 rows, got {len(rows)}')

    expected_history_name = expected_history
    correct = []
    rt = []
    for idx, r in enumerate(rows, start=1):
        try:
            trial = int(r['trial'])
        except (TypeError, ValueError):
            raise ValueError(f'{path}: trial {idx} is not an integer')
        if trial != idx:
            raise ValueError(f'{path}: trial numbering is not exactly 1..192 at row {idx}')
        if r['history'] != expected_history_name:
            raise ValueError(f'{path}: history mismatch at trial {idx}')
        try:
            c, x, y = (int(r[k]) for k in ('c', 'x', 'y'))
        except (TypeError, ValueError):
            raise ValueError(f'{path}: non-integer feature at trial {idx}')
        if c not in (0, 1) or x not in (0, 1) or y not in (0, 1):
            raise ValueError(f'{path}: non-binary feature at trial {idx}')
        if not r['production']:
            raise ValueError(f'{path}: missing production at trial {idx}')
        if r['action'] not in ('A0', ':A0', 'A1', ':A1'):
            raise ValueError(f'{path}: invalid action at trial {idx}')
        if r['correct_action'] not in ('A0', ':A0', 'A1', ':A1'):
            raise ValueError(f'{path}: invalid correct_action at trial {idx}')
        try:
            corr = int(r['correctness'])
            feedback = int(r['feedback'])
        except (TypeError, ValueError):
            raise ValueError(f'{path}: non-integer correctness/feedback at trial {idx}')
        if corr not in (0, 1):
            raise ValueError(f'{path}: correctness not binary at trial {idx}')
        if feedback != 1:
            raise ValueError(f'{path}: feedback is not exactly 1 at trial {idx}')
        try:
            this_rt = float(r['rt'])
        except (TypeError, ValueError):
            raise ValueError(f'{path}: invalid latency at trial {idx}')
        if not math.isfinite(this_rt) or this_rt < 0:
            raise ValueError(f'{path}: invalid latency value at trial {idx}')
        if not r['rng_state']:
            raise ValueError(f'{path}: missing rng_state at trial {idx}')
        correct.append(corr)
        rt.append(this_rt)

    seed_from_name = int(pathlib.Path(path).stem.split('-')[-1])
    if seed_from_name != expected_seed:
        raise ValueError(f'{path}: filename seed mismatch')
    acc = sum(correct) / len(correct)
    terminal = sum(correct[-32:]) / 32
    ttc = None
    for t in range(20, 193):
        if sum(correct[t-20:t]) >= 18:
            ttc = t
            break
    med_rt = statistics.median(rt)
    return {'path': path, 'history': expected_history_name, 'seed': expected_seed,
            'accuracy': acc, 'terminal_accuracy': terminal, 'ttc': ttc, 'median_rt': med_rt}


def pair(hs, hc):
    p = {}
    p['d_acc'] = hs['accuracy'] - hc['accuracy']
    p['d_terminal'] = hs['terminal_accuracy'] - hc['terminal_accuracy']
    if hs['ttc'] is None and hc['ttc'] is None:
        p['ttc_status'] = 'BOTH_NO_CRITERION'; p['ttc_pass'] = True; p['d_ttc'] = None
    elif hs['ttc'] is None or hc['ttc'] is None:
        p['ttc_status'] = 'ONE_NO_CRITERION'; p['ttc_pass'] = False; p['d_ttc'] = None
    else:
        p['ttc_status'] = 'BOTH_CRITERION'; p['d_ttc'] = hs['ttc'] - hc['ttc']; p['ttc_pass'] = abs(p['d_ttc']) <= TTC_TOL
    p['acc_pass'] = abs(p['d_acc']) <= ACC_TOL
    p['terminal_pass'] = abs(p['d_terminal']) <= ACC_TOL
    p['rt_ratio'] = hs['median_rt'] / hc['median_rt'] if hc['median_rt'] else None
    p['rt_pass'] = p['rt_ratio'] is not None and RT_LOW <= p['rt_ratio'] <= RT_HIGH
    p['all_pass'] = p['acc_pass'] and p['terminal_pass'] and p['ttc_pass'] and p['rt_pass']
    return p


def evaluate(result_dir, label):
    seeds = list(range(1001,1033)) if label == 'primary' else list(range(2001,2033))
    files = sorted(glob.glob(f'{result_dir}/H-S-{label}-*.csv'))
    if len(files) != 32:
        raise ValueError(f'{label}: expected 32 H-S runs, got {len(files)}')
    hs = {seed: load_run(f'{result_dir}/H-S-{label}-{seed}.csv', 'H-S', seed) for seed in seeds}
    hc_files = sorted(glob.glob(f'{result_dir}/H-C-{label}-*.csv'))
    if len(hc_files) != 32:
        raise ValueError(f'{label}: expected 32 H-C runs, got {len(hc_files)}')
    hc = {seed: load_run(f'{result_dir}/H-C-{label}-{seed}.csv', 'H-C', seed) for seed in seeds}
    if set(hs) != set(seeds) or set(hc) != set(seeds):
        raise ValueError(f'{label}: seed-set mismatch')
    pairs = {s: pair(hs[s], hc[s]) for s in seeds}
    def rate(k): return sum(bool(v[k]) for v in pairs.values()) / len(pairs)
    med_d_acc = statistics.median(v['d_acc'] for v in pairs.values())
    med_d_terminal = statistics.median(v['d_terminal'] for v in pairs.values())
    rt_vals = [v['rt_ratio'] for v in pairs.values() if v['rt_ratio'] is not None]
    med_rt_ratio = statistics.median(rt_vals) if rt_vals else None
    acc_pass = rate('acc_pass') >= PAIR_PASS_RATE and abs(med_d_acc) <= ACC_TOL
    terminal_pass = rate('terminal_pass') >= PAIR_PASS_RATE and abs(med_d_terminal) <= ACC_TOL
    ttc_pass = rate('ttc_pass') >= PAIR_PASS_RATE
    rt_pass = rate('rt_pass') >= PAIR_PASS_RATE and med_rt_ratio is not None and RT_LOW <= med_rt_ratio <= RT_HIGH
    overall = acc_pass and terminal_pass and ttc_pass and rt_pass
    return {'label': label, 'paired_seeds': seeds, 'component_pass_rates': {'accuracy': rate('acc_pass'), 'terminal_accuracy': rate('terminal_pass'), 'ttc': rate('ttc_pass'), 'latency': rate('rt_pass')}, 'median_d_acc': med_d_acc, 'median_d_terminal': med_d_terminal, 'median_rt_ratio': med_rt_ratio, 'component_pass': {'accuracy': acc_pass, 'terminal_accuracy': terminal_pass, 'ttc': ttc_pass, 'latency': rt_pass}, 'overall': overall, 'pairs': pairs}


def main():
    result_dir = sys.argv[1] if len(sys.argv) > 1 else 'h2-results'
    primary = evaluate(result_dir, 'primary')
    replication = evaluate(result_dir, 'replication')
    overall = primary['overall'] and replication['overall']
    out = {'primary': primary, 'replication': replication, 'matching': 'MATCH CONFIRMED' if overall else 'MATCH FAILURE'}
    pathlib.Path(result_dir, 'matching-decision.json').write_text(json.dumps(out, indent=2))
    print(json.dumps({'primary': primary['component_pass'], 'replication': replication['component_pass'], 'matching': out['matching']}, indent=2))
    raise SystemExit(0 if overall else 2)

if __name__ == '__main__': main()
