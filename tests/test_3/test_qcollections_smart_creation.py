import pytest
from quietude.quietude.blender_utils import bcollections
from quietude.quietude.core import qcollections

def test_qcollections_count():
    assert(bcollections.get_children_count('Quietude') == 3)

@pytest.mark.parametrize("qcollection_number, expected", [
    [1, ["Cube"]],
    [2, ["Cube", "Cylinder", "Cube.001"]],
    [3, ["Cube", "Cylinder"]]
])
def test_qcollections_members(qcollection_number, expected):
    assert(set(qcollections.get_qcollection_by_number(qcollection_number).objects.keys()) == set(expected))