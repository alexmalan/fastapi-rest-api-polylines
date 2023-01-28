"""
File management service.
"""
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from numpy import save


def save_nparray_to_file(nparray: "nparray", filename: str):
    """
    Save numpy array to file.

    Parameters
    ----------
    nparray : nparray
        Numpy array to save.
    filename : str
        The filename to save the numpy array to.
    """
    try:
        loc_path = Path(__file__).parents[1] / f"data/{filename}"

        # save the numpy array to the npy file
        save(loc_path, nparray)
        loc_path = loc_path.with_suffix(".npy")

        return loc_path
    except:
        raise ValueError("Something went wrong saving the file. Please try again.")


def save_matplot_figure(nparr: "nparray", filename: str):
    """
    Save matplotlib figure to file.

    Parameters
    ----------
    nparr : nparray
        Numpy array to save.
    filename : str
        The filename to save the plot to.
    """
    try:
        loc_path = Path(__file__).parents[1] / f"data/{filename}-plot.png"

        # check all the ones in the nparray and add them to the plot
        poly_check = np.where(nparr == 1)
        plt.plot(poly_check[0], poly_check[1])
        plt.savefig(loc_path)

        return loc_path
    except:
        raise ValueError("Something went wrong saving the file. Please try again.")
