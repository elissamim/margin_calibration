import numpy as np
import pytest
import sys
sys.path.append("../src")
from margin_calibration import MarginCalibration

sampling_probabilities = np.random.uniform(low=0, high=1, size=(10, 1))
calibration_matrix = np.random.uniform(low=0, high=100, size=(10, 2))
calibration_target = calibration_matrix.sum(axis=0)*100
calibration_target = calibration_target.reshape(-1, 1)

def test_linear_distance():
    
    mc=MarginCalibration(sampling_probabilities,
                        calibration_matrix,
                        calibration_target,
                        calibration_method = "linear")
    
    assert mc._linear_method(1, 1) == 0

def test_truncated_linear_distance():

    mc=MarginCalibration(sampling_probabilities,
                        calibration_matrix,
                        calibration_target,
                        calibration_method = "truncated_linear",
                        lower_bound = 0.5,
                        upper_bound = 1.5)
    
    assert mc._linear_method(1, 1) == 0

def test_logit_distance():

    mc=MarginCalibration(sampling_probabilities,
                        calibration_matrix,
                        calibration_target,
                        calibration_method = "logit",
                        lower_bound=0.5,
                        upper_bound=1.5)

    assert mc._logit_method(1, 1) == 0

def test_raking_ratio_distance():

    mc=MarginCalibration(sampling_probabilities,
                        calibration_matrix,
                        calibration_target,
                        calibration_method = "raking_ratio")
    
    assert mc._raking_ratio_method(1, 1) == 0

def test_ndarray_creator():

    mc=MarginCalibration(sampling_probabilities,
                        calibration_matrix,
                        calibration_target)

    assert all(isinstance(x, np.ndarray)
              for x in [mc.sampling_probabilities, mc.calibration_matrix, mc.calibration_target])
    
if __name__ == "__main__":
    pytest.main()

