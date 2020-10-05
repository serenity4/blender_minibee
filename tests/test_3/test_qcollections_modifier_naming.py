import pytest
from quietude.quietude.blender_utils import bmodifiers
from quietude.quietude.core import qcollections

@pytest.mark.parametrize("qcollection_number, expected_modifier_name", [
    [1, "Q1_MIRROR_1"],
    [2, "Q2_MIRROR_1"],
    [2, "Q2_MIRROR_2"],
    [3, "Q3_MIRROR_1"]
])
def test_modifier_naming(qcollection_number, expected_modifier_name):
    for obj in qcollections.get_qcollection_by_number(qcollection_number).objects:
        assert(bmodifiers.has_modifier(obj, expected_modifier_name))