import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

def check_nans(arr: np.ndarray, error_message: Optional[str] = None) -> None:
    """
    Checks if the given NumPy array contains NaN values.

    Args:
        arr (np.ndarray): The input array to check for NaN values.
        error_message (Optional[str], optional): Custom error message to raise if NaNs are found. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If NaN values are found in the array.
    """
    if np.isnan(arr).any():
        raise ValueError(error_message or "NaN values in the vector")
    return None

def check_zeros(arr: np.ndarray, error_message: Optional[str] = None) -> None:
    """
    Checks if the given NumPy array contains zero values.

    Args:
        arr (np.ndarray): The input array to check for zero values.
        error_message (Optional[str], optional): Custom error message to raise if zeros are found. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If zero values are found in the array.
    """
    if (arr == 0).any():
        raise ValueError(error_message or "Zero values in the vector")
    return None

def check_negative_values(arr: np.ndarray, error_message: Optional[str] = None) -> None:
    """
    Checks if the given NumPy array contains negative values.

    Args:
        arr (np.ndarray): The input array to check for negative values.
        error_message (Optional[str], optional): Custom error message to raise if negative values are found. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If negative values are found in the array.
    """
    if (arr < 0).any():
        raise ValueError(error_message or "Negative values in the vector")
    return None

def plot_density(arr: np.ndarray) -> None:
    """
    Plots the density distribution of an array.

    Args:
        arr (np.ndarray) : The input array containing the data to plot..

    Returns:
        None.
    """

    sns.set_style("white")

    plt.figure()

    ax = sns.kdeplot(
        arr,
        fill=True,
        alpha=.5,
        linewidth=1.25,
        color="#FF6666",
        bw_adjust=2
    )

    plt.xlabel("Calibration factors (w/d)")
    plt.ylabel("Density")
    plt.title("Density plot of the calibration factors")
    plt.tight_layout()

    plt.show()
    
    