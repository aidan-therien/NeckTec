import pytest
from datetime import datetime
from pymodm import connect, MongoModel, fields


@pytest.mark.parametrize('info, expected',
                         [({"phys_id": 1,
                            "neck_angles": [1.234, 2.3456, 3.4567, 4]},
                           [1, [1.234, 2.3456, 3.4567, 4]]),
                          ({"phys_id": 5,
                            "neck_angles": [1.4, 256, 67, 4]},
                           [5, [1.4, 256, 67, 4]])])
def test_add_new_patient(info, expected):
    from server import read_physician
    answer = read_physician(info)
    assert answer[0:2] == expected


@pytest.mark.parametrize("data, expected",
                         [({"phys_id": 1,
                            "data": 20.0}, True),
                          ({"phys_id": 123,
                            "data": '21'},
                           "data value is not the correct type"),
                          ({"phys_id": 1,
                            "age": 20},
                           "data key not found in input"),
                          ({"phys_id": '123',
                            "data": 21},
                           "phys_id value is not the correct type")])
def test_verify_new_patient_info(data, expected):
    from server import verify_input
    answer = verify_input(data)
    assert answer == expected


@pytest.mark.parametrize("data, expected",
                         [({"phys_id": 1,
                            "phys_name": "johnathan"}, True),
                          ({"phys_id": 123,
                            "phys_name": 1},
                           "phys_name value is not the correct type"),
                          ({"phys_id": 1,
                            "age": 20},
                           "phys_name key not found in input"),
                          ({"phys_id": '123',
                            "phys_name": 21},
                           "phys_id value is not the correct type")])
def test_verify_new_patient_info(data, expected):
    from server import verify_new_phys
    answer = verify_new_phys(data)
    assert answer == expected
