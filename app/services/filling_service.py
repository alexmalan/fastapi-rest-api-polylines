"""
Polygon filling service.
"""
import math
from datetime import datetime

import numpy as np
from skimage.draw import polygon


def fill_polyline(polygon_points, algorithm, flood_x=None, flood_y=None):
    """
    Method for handling algorithm selection.

    Parameters
    ----------
    arr : list
        Array of points that define the polygon.
    algorithm : str
        Algorithm to use for filling the polygon.

    Returns
    -------
    numpy.ndarray
        Array of points that define the filled polygon.
    execution_time : float
        Time taken to fill and process the polygon.
    """
    nparr = np.zeros((19200, 10800), dtype=np.uint8)

    if algorithm in ["rourke", "fast"]:
        start_time = datetime.now()
        rows, columns = [], []

        # prepare the x y points
        for i in range(len(polygon_points)):
            rows.append(polygon_points[i][0])
            columns.append(polygon_points[i][1])

        if algorithm == "rourke":
            result = fill_polyline_rourke(rows, columns, nparr)
        if algorithm == "fast":
            result = fill_polygon_fast(nparr, rows, columns)

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        return (result, execution_time)
    elif algorithm == "flood":
        start_time = datetime.now()
        fill_points = []
        polygon_points.append(polygon_points[0])

        # apply bresemham's line algorithm to each pair of points
        for i in range(len(polygon_points) - 1):
            fill_points.extend(
                list(
                    bresenham(
                        polygon_points[i][0],
                        polygon_points[i][1],
                        polygon_points[i + 1][0],
                        polygon_points[i + 1][1],
                    )
                )
            )

        # Fill the points
        xarr, yarr = [], []
        for i in fill_points:
            nparr[i[0]][i[1]] = 1
            xarr.append(i[0])
            yarr.append(i[1])

        if flood_x and flood_y:
            flood_fill_4(flood_x, flood_y, 0, 1, nparr)
        else:
            # find the latter points of the polygon
            min_x = min(xarr)
            max_x = max(xarr)
            min_y = min(yarr)
            max_y = max(yarr)

            # compute the center of the polygon
            x_start = max_x - (max_x - min_x)
            y_start = max_y - (max_y - min_y)

            # Fill the polygon recursively
            flood_fill_4(x_start, y_start, 0, 1, nparr)

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        return (nparr, execution_time)
    else:
        raise ValueError("Invalid algorithm.")


def fill_polygon_fast(nparr, rows, columns):
    """
    Fill a polygon defined by a list of points.

    Parameters
    ----------
    points : list of tuples
        List of points that define the polygon.

    Returns
    -------
    numpy.ndarray
        Array of points that define the filled polygon.

    """
    try:
        row_values, column_values = polygon(rows, columns)
        nparr[row_values, column_values] = 1

        return nparr
    except:
        raise ValueError("Something went wrong filling the polygon. Please try again.")


def flood_fill_4(x, y, old, new, arr):
    """
    Flood fill algorithm for 4-connected pixels.

    Parameters
    ----------
    x : int
        X coordinate of the start position.
    y : int
        Y coordinate of the start position.
    old : int
        Old value.
    new : int
        New value.
    arr : numpy.ndarray
        Array of points that define the filled polygon.
    """
    # the flood fill has 4 parts
    # firstly, make sure the x and y are inbounds
    if x < 0 or x >= len(arr[0]) or y < 0 or y >= len(arr):
        return

    # secondly, check if the current position equals the old value
    if arr[y][x] != old:
        return

    # thirdly, set the current position to the new value
    arr[y][x] = new

    # fourthly, attempt to fill the neighboring positions
    flood_fill_4(x + 1, y, old, new, arr)
    flood_fill_4(x - 1, y, old, new, arr)
    flood_fill_4(x, y + 1, old, new, arr)
    flood_fill_4(x, y - 1, old, new, arr)


def bresenham(x0, y0, x1, y1):
    """
    Bresenham's line algorithm.

    Used to draw lines from one point to another.
    Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.

    The result will contain both the start and the end point.

    Parameters
    ----------
    x0 : int
        X coordinate of the start position.
    y0 : int
        Y coordinate of the start position.
    x1 : int
        X coordinate of the end position.
    y1 : int
        Y coordinate of the end position.

    Yield
    -------
    list
        List of points that define the line.
    """

    # calculate delta x and delta y
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    # get abs value of delta x and delta y
    dx = abs(dx)
    dy = abs(dy)

    # compare delta x and delta y
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    # calculate slope based on P value
    for x in range(dx + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy


def point_in_polygons(column_points, row_points, column_i, row_i):
    """
    Test relative point position to a polygon.

    Parameters
    ----------
    column_points : nparray
        Array of x coordinates of the polygon.
    row_points : nparray
        Array of y coordinates of the polygon.
    column_i : int
        X coordinate of the point.
    row_i : int
        Y coordinate of the point.

    Returns
    -------
    c : Point relative position to the polygon
        O: outside
        1: inside
        2: vertex
        3: edge.
    """
    nr_vertices = column_points.shape[0]

    x0 = np.float64(0.0)
    x1 = np.float64(0.0)
    y0 = np.float64(0.0)
    y1 = np.float64(0.0)

    l_cross = 0
    r_cross = 0

    # Tolerance for vertices labelling
    eps = 1e-12

    # Initialization the loop
    x1 = column_points[nr_vertices - 1] - column_i
    y1 = row_points[nr_vertices - 1] - row_i

    # For each edge e = (i-1, i), see if it crosses ray
    for vertice in range(nr_vertices):
        x0 = column_points[vertice] - column_i
        y0 = row_points[vertice] - row_i

        if (-eps < x0 < eps) and (-eps < y0 < eps):
            # it is a vertex with an eps tolerance
            return 2

        # if e straddles the x-axis
        if (y0 > 0) != (y1 > 0):
            # check if it crosses the ray
            if ((x0 * y1 - x1 * y0) / (y1 - y0)) > 0:
                r_cross += 1
        # if reversed e straddles the x-axis
        if (y0 < 0) != (y1 < 0):
            # check if it crosses the ray
            if ((x0 * y1 - x1 * y0) / (y1 - y0)) < 0:
                l_cross += 1

        x1 = x0
        y1 = y0

    if (r_cross & 1) != (l_cross & 1):
        # on edge if left and right crossings not of same parity
        return 3

    if r_cross & 1:
        # inside if odd number of crossings
        return 1

    # outside if even number of crossings
    return 0


def fill_polyline_rourke(row, column, nparr):
    """
    Generate coordinates of pixels within polygon.

    Parameters
    ----------
    row : ndarray
        Row coordinates of vertices of polygon.
    column : ndarray
        Column coordinates of vertices of polygon.
    nparr : ndarray
        Array of points that define the filled polygon.
    Returns
    -------
    nparr : numpy.ndarray
        Array of points that define the filled polygon.
    """
    # check dimension of array
    rows = np.atleast_1d(row)
    columns = np.atleast_1d(column)

    # check minimum and maximum row and column values
    min_row = int(max(0, rows.min()))
    max_row = int(math.ceil(rows.max()))
    min_column = int(max(0, columns.min()))
    max_column = int(math.ceil(columns.max()))

    # make contiguous arrays of row and column coordinates
    # faster access in memory if they are next to each other
    row_points = np.ascontiguousarray(rows, "float64")
    column_points = np.ascontiguousarray(columns, "float64")

    # define output coordinate arrays
    row_coord_output = []
    column_coord_output = []

    # verify points in polygon
    for row_i in range(min_row, max_row + 1):
        for column_i in range(min_column, max_column + 1):
            if point_in_polygons(column_points, row_points, column_i, row_i):
                row_coord_output.append(row_i)
                column_coord_output.append(column_i)
    nparr[row_coord_output, column_coord_output] = 1

    return nparr
