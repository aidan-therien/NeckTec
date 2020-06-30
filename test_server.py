import pytest
from pymodm import connect, MongoModel, fields


@pytest.mark.parametrize('info, expected',
                         [({"phys_id": 1,
                            "neck_angles": [1.234, 2.3456, 3.4567, 4],
                            "timestamp": ["4", "5", "6"]},
                           [1, [1.234, 2.3456, 3.4567, 4], ["4", "5", "6"]]),
                          ({"phys_id": 5,
                            "neck_angles": [1.4, 256, 67, 4],
                            "timestamp": ["4", "5", "6"]},
                           [5, [1.4, 256, 67, 4], ["4", "5", "6"]])])
def test_add_new_patient(info, expected):
    from server import read_physician
    answer = read_physician(info)
    assert answer == expected

