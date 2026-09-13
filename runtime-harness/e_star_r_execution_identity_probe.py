from __future__ import print_function
import hashlib
import json
import os
import platform
import random
import subprocess
import sys
import types

import numpy
import pygame

EXPECTED = {
    'DORA.py': 'fdb40ef14706fbd0f0cb33e201e0e1af604ee71d',
    'basicRunDORA.py': 'a595db84e0da73d3cfb36fb0afab44cb53116db0',
}
REPLAY_SEED = 20260913
WORKSPACE = os.getcwd()


def hbytes(value):
    return hashlib.sha256(value).hexdigest()


def hfile(path):
    with open(path, 'rb') as fh:
        return hbytes(fh.read())


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def py_rng_hash(state):
    return hbytes(repr(state).encode('utf-8'))


def np_rng_hash(state):
    alg, keys, pos, has_gauss, cached = state
    payload = '%s|%s|%s|%s|%s|%s' % (
        alg, str(keys.dtype), keys.shape, keys.tostring().encode('hex'),
        int(pos), '%s|%s' % (int(has_gauss), float(cached)))
    return hbytes(payload.encode('utf-8'))


def canonical_params_hash(params):
    return hbytes(stable(params).encode('utf-8'))


def object_fingerprint(obj):
    # Constructor baseline is intentionally limited to source-created object
    # state; it is not the E*-R experimental S0.
    def encode(v, seen):
        if v is None or isinstance(v, (bool, int, float, str, unicode)):
            return v
        if isinstance(v, dict):
            return dict((str(k), encode(x, seen)) for k, x in sorted(v.items(), key=lambda p: str(p[0])))
        if isinstance(v, (list, tuple)):
            return [encode(x, seen) for x in v]
        marker = id(v)
        if marker in seen:
            return {'__cycle__': True}
        seen.add(marker)
        if hasattr(v, 'tostring') and hasattr(v, 'dtype') and hasattr(v, 'shape'):
            return {'__ndarray__': True, 'dtype': str(v.dtype), 'shape': list(v.shape), 'sha256': hbytes(v.tostring())}
        if hasattr(v, '__dict__'):
            return {'__class__': v.__class__.__name__, '__module__': v.__class__.__module__, '__dict__': encode(v.__dict__, seen)}
        return repr(v)
    return hbytes(stable(encode(obj, set())).encode('utf-8'))


# Exact source verification before controlled in-memory loading.
for name, expected in EXPECTED.items():
    path = os.path.join(WORKSPACE, name)
    actual = subprocess.check_output(['git', 'hash-object', path]).strip()
    assert actual == expected, (name, actual, expected)

source_path = os.path.join(WORKSPACE, 'DORA.py')
with open(source_path, 'rb') as fh:
    source = fh.read().decode('utf-8')
marker = '##############################################################################\n###########################        MAIN BODY        ##########################\n##############################################################################'
assert marker in source
controlled = source.split(marker, 1)[0]

mod = types.ModuleType('DORA')
mod.__file__ = source_path
mod.__package__ = ''
sys.modules['DORA'] = mod
exec(compile(controlled, source_path + '::controlled-load', 'exec', dont_inherit=True), mod.__dict__)

import DORA
import basicRunDORA
import buildNetwork
import dataTypes
import DORA_GUI

params = DORA.parameters
expected_keys = set([
    'asDORA', 'gamma', 'delta', 'eta', 'HebbBias', 'lateral_input_level',
    'strategic_mapping', 'ignore_object_semantics', 'ignore_memory_semantics',
    'mag_decimal_precision', 'dim_list', 'exemplar_memory',
    'recent_analog_bias', 'bias_retrieval_analogs', 'use_relative_act',
    'run_order', 'run_cyles', 'write_on_iteration', 'firingOrderRule',
    'screen_width', 'screen_height', 'doGUI', 'GUI_update_rate',
    'starting_iteration'
])
assert set(params.keys()) == expected_keys
assert params['firingOrderRule'] == 'random'
parameter_profile_sha256 = canonical_params_hash(params)

# Runtime/container identity.
interpreter_sha256 = hfile(sys.executable)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
repo_manifest = subprocess.check_output(['git', 'ls-tree', '-r', '--full-tree', 'HEAD']).strip()
repo_manifest_sha256 = hbytes(repo_manifest)
os_release = ''
if os.path.isfile('/etc/os-release'):
    with open('/etc/os-release', 'rb') as fh:
        os_release = fh.read()
os_release_sha256 = hbytes(os_release)
env_material = '\n'.join(k + '=' + os.environ[k] for k in sorted(os.environ))
environment_variables_sha256 = hbytes(env_material.encode('utf-8'))

# Resource inventory: every repository-local Python module actually imported
# by the controlled construction path, plus their immutable Git blob identity.
resources = {}
workspace_abs = os.path.abspath(WORKSPACE)
for name, module in sorted(sys.modules.items()):
    path = getattr(module, '__file__', None)
    if not path:
        continue
    path = os.path.abspath(path)
    if not path.startswith(workspace_abs + os.sep):
        continue
    if path.endswith('.pyc'):
        path = path[:-1]
    if os.path.isfile(path):
        rel = os.path.relpath(path, workspace_abs)
        resources[rel] = subprocess.check_output(['git', 'hash-object', path]).strip()
resource_manifest_sha256 = hbytes(stable(resources).encode('utf-8'))

# External dependency identities as installed package trees.
def package_tree_sha(module):
    root = os.path.abspath(module.__file__)
    if os.path.isfile(root):
        root = os.path.dirname(root)
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort(); filenames.sort()
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            entries.append(os.path.relpath(path, root) + '\t' + hfile(path))
    return hbytes('\n'.join(entries).encode('utf-8'))

numpy_tree_sha256 = package_tree_sha(numpy)
pygame_tree_sha256 = package_tree_sha(pygame)

# Technical constructor replay only. The seed is explicitly NOT the E*-R
# experimental seed, and the replay baseline is explicitly NOT experimental S0.
random.seed(REPLAY_SEED)
numpy.random.seed(REPLAY_SEED)
py_before_a = random.getstate()
np_before_a = numpy.random.get_state()
network_a = basicRunDORA.runDORA(dataTypes.memorySet(), params)
state_a = object_fingerprint(network_a)
py_after_a = random.getstate()
np_after_a = numpy.random.get_state()

random.seed(REPLAY_SEED)
numpy.random.seed(REPLAY_SEED)
py_before_b = random.getstate()
np_before_b = numpy.random.get_state()
network_b = basicRunDORA.runDORA(dataTypes.memorySet(), params)
state_b = object_fingerprint(network_b)
py_after_b = random.getstate()
np_after_b = numpy.random.get_state()

assert py_rng_hash(py_before_a) == py_rng_hash(py_before_b)
assert np_rng_hash(np_before_a) == np_rng_hash(np_before_b)
assert state_a == state_b
assert py_rng_hash(py_after_a) == py_rng_hash(py_after_b)
assert np_rng_hash(np_after_a) == np_rng_hash(np_after_b)

print('FULL_PARAMETER_PROFILE=PASS')
print('PARAMETER_PROFILE_KEYS_EXACT=PASS')
print('RESOURCE_INVENTORY=PASS')
print('RUNTIME_CONSTRUCTOR_REPLAY=PASS')
print('E_STAR_R_EXECUTION=NOT_RUN')
print('E_STAR_R_S0=UNRESOLVED')
print('E_STAR_R_ADAPTER=UNRESOLVED')
print('PYTHON=%s' % platform.python_version())
print('PYTHON_EXECUTABLE=%s' % sys.executable)
print('PYTHON_EXECUTABLE_SHA256=%s' % interpreter_sha256)
print('NUMPY=%s' % numpy.__version__)
print('NUMPY_INSTALLED_TREE_SHA256=%s' % numpy_tree_sha256)
print('PYGAME=%s' % pygame.version.ver)
print('PYGAME_INSTALLED_TREE_SHA256=%s' % pygame_tree_sha256)
print('GIT_COMMIT=%s' % commit)
print('GIT_REPOSITORY_MANIFEST_SHA256=%s' % repo_manifest_sha256)
print('GIT_BLOB_SHA_DORA=%s' % EXPECTED['DORA.py'])
print('GIT_BLOB_SHA_BASICRUNDORA=%s' % EXPECTED['basicRunDORA.py'])
print('RESOURCE_MANIFEST_SHA256=%s' % resource_manifest_sha256)
print('RESOURCE_MANIFEST=%s' % stable(resources))
print('OS_RELEASE_SHA256=%s' % os_release_sha256)
print('PLATFORM_UNAME=%s' % stable(platform.uname()))
print('ENVIRONMENT_VARIABLES_SHA256=%s' % environment_variables_sha256)
print('WORKING_DIRECTORY_HASH=%s' % repo_manifest_sha256)
print('PARAMETER_PROFILE_SHA256=%s' % parameter_profile_sha256)
print('RUNTIME_REPLAY_SEED=%d' % REPLAY_SEED)
print('RUNTIME_REPLAY_PYTHON_STATE_BEFORE_SHA256=%s' % py_rng_hash(py_before_a))
print('RUNTIME_REPLAY_NUMPY_STATE_BEFORE_SHA256=%s' % np_rng_hash(np_before_a))
print('RUNTIME_REPLAY_PYTHON_STATE_AFTER_SHA256=%s' % py_rng_hash(py_after_a))
print('RUNTIME_REPLAY_NUMPY_STATE_AFTER_SHA256=%s' % np_rng_hash(np_after_a))
print('CONSTRUCTOR_BASELINE_STATE_SHA256=%s' % state_a)
print('CONTROLLED_LOAD_EXCLUDED_INTERACTIVE_MAIN_BODY=True')
