#!/usr/bin/env python3
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
EXPECTED = {
    'envelope': 'c0c76b6cccd5d3eca97005c7fa7932803356852b',
    'lock': 'c0536f8a0484ad73c62d030c9096a34895e777ae',
    'fixture': '10dc5cfb8a14774d77e951e106c575e289c15bf5503c611ec420c997ae33d32d',
}
PRIMARY = list(range(1001,1033))
REPLICATION = list(range(2001,2033))

def fail(msg):
    print('AUDIT FAIL: ' + msg)
    raise SystemExit(1)

def main():
    manifest_path = ROOT / 'H2-MATCHING-IMPLEMENTATION-MANIFEST-v0.1.json'
    model_path = ROOT / 'H2-MATCHING-MODEL-v0.1.lisp'
    runner_path = ROOT / 'run-h2-matching.lisp'
    if not all(p.exists() for p in (manifest_path, model_path, runner_path)):
        fail('required implementation artifact missing')
    manifest = json.loads(manifest_path.read_text())
    pre = manifest['pre_implementation']
    if pre['capability_envelope_sha'] != EXPECTED['envelope']:
        fail('capability envelope SHA mismatch')
    if pre['lock_record_sha'] != EXPECTED['lock']:
        fail('lock-record SHA mismatch')
    if manifest['fixture']['sha256'] != EXPECTED['fixture']:
        fail('complete fixture SHA mismatch')
    if manifest['seeds']['primary'] != PRIMARY or manifest['seeds']['replication'] != REPLICATION:
        fail('seed policy mismatch')
    model = model_path.read_text()
    runner = runner_path.read_text()
    for required in [':ult t', ':esc t', ':ul t', ':alpha 0.2', ':iu 0', ':egs 0', ':er t', ':epl nil', 'chunk-type h2-goal c x y']:
        if required not in model:
            fail('missing frozen declaration: ' + required)
    if re.search(r'chunk-type\s+h2-goal[^\n]*?(?:xor|relation|rule|structure|correct-action)', model, re.I):
        fail('forbidden learner slot detected')
    if '(trigger-reward' not in runner:
        fail('reward mechanism missing')
    if '"H2-W0.3-TRAINING-ONLY.csv"' not in runner:
        fail('fixed training fixture boundary missing')
    for phrase in ['select best seed', 'remove seed', 'choose seed', 'widen tolerance', 'replace history', 'parameter sweep', 'grid search']:
        if phrase in (runner + model).lower():
            fail('post-hoc selection/tuning path detected: ' + phrase)
    if 'future fixture' in runner.lower() or 'a_to_d_forward_prediction_generated' in runner.lower():
        fail('future prediction path detected')
    if 'run-h2-history-seed' not in runner:
        fail('execution entrypoint missing')
    print('AUDIT PASS: frozen SHAs, representation, mechanisms, parameters, fixture boundary, seeds, reward path, and post-hoc prohibition checks passed')

if __name__ == '__main__':
    main()
