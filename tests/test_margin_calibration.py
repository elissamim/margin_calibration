import numpy as np
import pytest
import sys
sys.path.append("../src")
from margin_calibration import MarginCalibration
from utils import (
                    check_nans,
                    check_zeros,
                    check_negative_values
                   )

test_array = np.array([[1,2,3],[np.nan,3,4],[np.nan, -1,1],[0,0,0]])

def test_linear_distance():
    
    mc=MarginCalibration()
    
    assert mc._linear_method(1, 1) == 0

def test_logit_distance():

    mc=MarginCalibration(lower_bound=.9, upper_bound=1.1)

    assert mc._logit_method(1, 1) == 0

def test_raking_ratio_distance():

    mc=MarginCalibration()
    
    assert mc._raking_ratio_method(1, 1) == 0

def test_error_nans():

    with pytest.raises(ValueError):
        check_nans(test_array)

def test_error_zeros():

    with pytest.raises(ValueError):
        check_zeros(test_array)

def test_error_negatives():

    with pytest.raises(ValueError):
        check_negative_values(test_array)
    
if __name__ == "__main__":
    pytest.main()