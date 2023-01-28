"""
Poly service tests.
"""
from fastapi.testclient import TestClient

from app.services import fill_polyline
from main import app

client = TestClient(app)


def test_rectangle_fast():
    """
    Testing a rectangle shape within the np.array
    using skimage.draw.polygon

    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    .............................

    shape = (19200, 10800)
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


def test_triangle_fast():
    """
    Testing a triangle shape within the np.array
    using skimage.draw.polygon

    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    0 1 0 0 0 0 0 0 0 0 0 0 0 ...
    0 1 1 0 0 0 0 0 0 0 0 0 0 ...
    0 1 1 1 0 0 0 0 0 0 0 0 0 ...
    0 1 1 1 1 0 0 0 0 0 0 0 0 ...
    0 1 1 1 1 1 0 0 0 0 0 0 0 ...
    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    .............................

    shape = (19200, 10800)
    """
    points = [[1, 1], [5, 5], [5, 1]]
    result = fill_polyline(points, "fast")

    assert result[0].shape == (19200, 10800)
    assert (0 in result[0][0][1:6]) == True
    assert (0 in [result[0][1][1]]) == False
    assert (0 in result[0][2][1:2]) == False
    assert (0 in result[0][3][1:3]) == False
    assert (0 in result[0][4][1:4]) == False
    assert (0 in result[0][5][1:5]) == False
    assert (0 in result[0][6][1:6]) == True


def test_rectangle_rourke():
    """
    Testing a rectangle shape within the np.array
    using rourke algorithm

    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    .............................

    shape = (19200, 10800)
    """
    points = [[1, 1], [1, 2], [1, 5], [3, 5], [5, 5], [5, 3], [5, 1]]
    result = fill_polyline(points, "rourke")

    assert result[0].shape == (19200, 10800)
    assert (0 in result[0][0][1:6]) == True
    assert (0 in result[0][1][1:6]) == False
    assert (0 in result[0][2][1:6]) == False
    assert (0 in result[0][3][1:6]) == False
    assert (0 in result[0][4][1:6]) == False
    assert (0 in result[0][5][1:6]) == False
    assert (0 in result[0][6][1:6]) == True


def test_rectangle_flood():
    """
    Testing a rectangle shape within the np.array
    using 4-connectivity flood fill algorithm

    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 1 1 1 1 1 1 0 0 0 0 0 0 ...
    0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    .............................

    shape = (19200, 10800)
    """
    points = [[1, 1], [1, 2], [1, 5], [3, 5], [5, 5], [5, 3], [5, 1]]
    result = fill_polyline(points, "flood", 3, 3)

    assert result[0].shape == (19200, 10800)
    assert (0 in result[0][0][1:6]) == True
    assert (0 in result[0][1][1:6]) == False
    assert (0 in result[0][2][1:6]) == False
    assert (0 in result[0][3][1:6]) == False
    assert (0 in result[0][4][1:6]) == False
    assert (0 in result[0][5][1:6]) == False
    assert (0 in result[0][6][1:6]) == True
