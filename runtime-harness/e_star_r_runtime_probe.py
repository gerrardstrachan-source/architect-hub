from __future__ import print_function

import hashlib
import os
import platform
import sys
import types

import numpy
import pygame

EXPECTED = {
    "DORA.py": "fdb40ef14706fbd0f0cb33e201e0e1af604ee71d",
    "basicRunDORA.py": "a595db84e0da73d3cfb36fb0afab44cb53116db0",
}

workspace = os.getcwd()

# Verify exact pinned source bytes before controlled loading.
for name, digest in EXPECTED.items():
    path = os.path.join(workspace, name)
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        h.update(fh.read())
    actual = h.hexdigest()
    assert actual == digest, (name, actual, digest)

# DORA.py is an interactive executable and enters its MainMenu loop at module
# level. Leave the pinned source untouched. Load its declarations/definitions
# into a module namespace while excluding only that interactive entry-point
# block in memory.
source_path = os.path.join(workspace, "DORA.py")
with open(source_path, "rb") as fh:
    source_text = fh.read().decode("utf-8")
marker = "##############################################################################\n###########################        MAIN BODY        ##########################\n##############################################################################"
assert marker in source_text
controlled_text = source_text.split(marker, 1)[0]

module = types.ModuleType("DORA")
module.__file__ = source_path
module.__package__ = ""
sys.modules["DORA"] = module
exec(compile(controlled_text, source_path + "::controlled-load", "exec"), module.__dict__)

import DORA
import basicRunDORA
import buildNetwork
import dataTypes
import DORA_GUI

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

print("CONTROLLED_SOURCE_LOAD=PASS")
print("IMPORT_AND_CONSTRUCTION=PASS")
print("PYTHON=" + platform.python_version())
print("PYTHON_EXECUTABLE=" + sys.executable)
print("NUMPY=" + numpy.__version__)
print("PYGAME=" + pygame.version.ver)
print("DORA_VERSION=" + DORA.vers_number)
print("FIRING_ORDER_RULE=" + params["firingOrderRule"])
print("SOURCE_SHA1_DORA=" + EXPECTED["DORA.py"])
print("SOURCE_SHA1_BASICRUNDORA=" + EXPECTED["basicRunDORA.py"])
print("CONTROLLED_LOAD_EXCLUDED_INTERACTIVE_MAIN_BODY=True")
