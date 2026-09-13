#!/usr/bin/env python3
import hashlib, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent
EXPECTED = {
    'envelope': 'c0c76b6cccd5d3eca97005c7fa7932803356852b',
    'lock': 'c0536f8a0484ad73c62d030c9096a34895e777ae',
    'fixture': '10dc5cfb8a14774d77e951e106c575e289c15bf5503c611ec420c997ae33d32d',
    'model_blob_sha': 'b975c98274cd78867ed0c5dd0ea8d84189a861d9',
    'controller_blob_sha': '58cde21131cee94089bf14ab9ccbf9d4bb838396',
}
PRIMARY = list(range(1001,1033))
REPLICATION = list(range(2001,2033))

def fail(msg):
    print('AUDIT FAIL: ' + msg)
    raise SystemExit(1)

def git_blob_sha(path):
    data = pathlib.Path(path).read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

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
    if manifest['implementation']['model_blob_sha'] != EXPECTED['model_blob_sha']:
        fail('manifest model blob SHA mismatch')
    if manifest['implementation']['controller_blob_sha'] != EXPECTED['controller_blob_sha']:
        fail('manifest controller blob SHA mismatch')
    if git_blob_sha(model_path) != EXPECTED['model_blob_sha']:
        fail('checked-out model blob SHA mismatch')
    if git_blob_sha(runner_path) != EXPECTED['controller_blob_sha']:
        fail('checked-out controller blob SHA mismatch')
    if manifest['seeds']['primary'] != PRIMARY or manifest['seeds']['replication'] != REPLICATION:
        fail('seed policy mismatch')
    model = model_path.read_text()
    runner = runner_path.read_text()
    for required in [':ult t', ':esc t', ':ul t', ':alpha 0.2', ':iu 0', ':egs 0', ':er t', ':epl nil', 'chunk-type h2-goal c x y']:
        if required not in model:
            fail('missing frozen declaration: ' + required)
    if re.search(r'chunk-type\s+h2-goal[^\n]*?(?:xor|relation|rule|structure|correct-action)', model, re.I):
        fail('forbidden learner slot detected')
    for forbidden in ['define-chunks\s*\\n.*xor', 'define-chunks.*relation', 'chunk-type.*structure']:
        if re.search(forbidden, model, re.I | re.S):
            fail('forbidden representational encoding detected')
    if '(trigger-reward' not in runner or '(mp-time)' not in runner:
        fail('required reward/timing instrumentation missing')
    if '"H2-W0.3-TRAINING-ONLY.csv"' not in runner:
        fail('fixed training fixture boundary missing')
    if '*h2-training-sequence-codes*' not in runner:
        fail('frozen training sequence check missing')
    if 'H2 fixture rejected: ground-truth contingency mismatch' not in runner:
        fail('contingency verification missing')
    if 'future fixture' in runner.lower() or 'a_to_d_forward_prediction_generated' in runner.lower():
        fail('future prediction/access path detected')
    for phrase in ['select best seed', 'remove seed', 'choose seed', 'widen tolerance', 'replace history', 'parameter sweep', 'grid search']:
        if phrase in (runner + model).lower():
            fail('post-hoc selection/tuning path detected: ' + phrase)
    print('AUDIT PASS: pre-lock SHAs, checked-out implementation identities, learner representation, frozen mechanisms/parameters, exact training boundary, exact sequence, contingency validation, timing/reward instrumentation, and post-hoc prohibition checks passed')

if __name__ == '__main__':
    main()
