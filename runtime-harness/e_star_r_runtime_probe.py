from __future__ import print_function

import hashlib
import os
import platform
import sys

import numpy
import pygame
import DORA
import basicRunDORA
import buildNetwork
import dataTypes
import DORA_GUI

EXPECTED = {
    "DORA.py": "fdb40ef14706fbd0f0cb33e201e0e1af604ee71d",
    "basicRunDORA.py": "a595db84e0da73d3cfb36fb0afab44cb53116db0",
}

for name, digest in EXPECTED.items():
    path = os.path.join(os.getcwd(), name)
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        h.update(fh.read())
    actual = h.hexdigest()
    assert actual == digest, (name, actual, digest)

params = DORA.parameters
required = [
    "asDORA", "gamma", "delta", "eta", "HebbBias",
    "bias_retrieval_analogs", "use_relative_act", "run_order",
    "run_cyles", "write_on_iteration", "firingOrderRule",
    "strategic_mapping", "ignore_object_semantics", "ignore_memory_semantics",
    "mag_decimal_precision", "dim_list", "exemplar_memory", "recent_analog_bias",
    "lateral_input_level", "screen_width", "screen_height", "doGUI",
    "GUI_update_rate", "starting_iteration",
]
missing = [key for key in required if key not in params]
assert not missing, missing

network = basicRunDORA.runDORA(None, params)
assert network.firingOrderRule == "random"
assert network.gamma == params["gamma"]
assert network.delta == params["delta"]
assert network.eta == params["eta"]
assert network.HebbBias == params["HebbBias"]

print("IMPORT_AND_CONSTRUCTION=PASS")
print("PYTHON=" + platform.python_version())
print("PYTHON_EXECUTABLE=" + sys.executable)
print("NUMPY=" + numpy.__version__)
print("PYGAME=" + pygame.version.ver)
print("DORA_VERSION=" + DORA.vers_number)
print("FIRING_ORDER_RULE=" + params["firingOrderRule"])
print("SOURCE_SHA1_DORA=" + EXPECTED["DORA.py"])
print("SOURCE_SHA1_BASICRUNDORA=" + EXPECTED["basicRunDORA.py"])
