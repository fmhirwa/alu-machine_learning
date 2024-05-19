#!/usr/bin/env python3
""" Documentation"""


import numpy as np


def np_cat(mat1, mat2, axis=0):
    """
        function that Concatenate two arrays based on an axis
    """
    return np.concatenate((mat1, mat2), axis=axis)
