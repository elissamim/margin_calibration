import numpy as np
import pytest
import sys
sys.path.append("../src")
from margin_calibration import MarginCalibration

def test_pseudo_distance_functions():
    
    sampling_probabilities = np.random.uniform(low=0, high=1, size=(10, 1))
    calibration_matrix = np.random.uniform(low=0, high=100, size=(10, 2))
    calibration_target = calibration_matrix.sum(axis=0)*100
    calibration_target = calibration_target.reshape(-1, 1)
    
    dict_methods = {
        "linear":_linear_method,
        "truncated_linear":_linear_method,
        "logit":_logit_method,
        "ranking_ratio":_ranking_ratio_method
    }

    for method in dict_methods.keys():
        mc=MarginCalibration(sampling_probabilities,
                            calibration_matrix,
                            calibration_target,
                            calibration_method = method)
        assert mc.dict_methods[method](1, 1) == 0



if __name__ == "__main__":
    pytest.main()

