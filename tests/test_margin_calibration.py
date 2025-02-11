import numpy as np
import pytest
import sys
sys.path.append("../src")
from margin_calibration import MarginCalibration

def test_linear_distance():
    
    mc=MarginCalibration()
    
    assert mc._linear_method(1, 1) == 0

def test_logit_distance():

    mc=MarginCalibration(lower_bound=.9, upper_bound=1.1)

    assert mc._logit_method(1, 1) == 0

def test_raking_ratio_distance():

    mc=MarginCalibration()
    
    assert mc._raking_ratio_method(1, 1) == 0
    
if __name__ == "__main__":
    pytest.main()

