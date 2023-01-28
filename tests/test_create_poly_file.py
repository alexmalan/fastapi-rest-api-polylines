"""
Poly service tests.
"""
import os

from fastapi.testclient import TestClient
from numpy import load

from app.services import fill_polyline, save_nparray_to_file
from main import app

client = TestClient(app)


def tests_create_poly():
    """
    Test creating a poly item.
    """
    points = [[1, 1], [1, 2], [1, 5], [3, 5], [5, 5], [5, 3], [5, 1]]
    result = fill_polyline(points, "fast")

    assert result[0].shape == (19200, 10800)
    assert (0 in result[0][0][1:6]) == True
    assert (0 in result[0][1][1:6]) == False
    assert (0 in result[0][2][1:6]) == False
    assert (0 in result[0][3][1:6]) == False
    assert (0 in result[0][4][1:6]) == False
    assert (0 in result[0][5][1:6]) == False
    assert (0 in result[0][6][1:6]) == True

    # test saving the np.array to a file .NPY
    save_file = save_nparray_to_file(result[0], "test_poly")
    loaded_arr = load(save_file)

    assert loaded_arr.shape == (19200, 10800)
    assert (0 in loaded_arr[0][1:6]) == True
    assert (0 in loaded_arr[1][1:6]) == False
    assert (0 in loaded_arr[2][1:6]) == False
    assert (0 in loaded_arr[3][1:6]) == False
    assert (0 in loaded_arr[4][1:6]) == False
    assert (0 in loaded_arr[5][1:6]) == False
    assert (0 in loaded_arr[6][1:6]) == True

    # remove the file
    if os.path.isfile(save_file):
        os.remove(save_file)
