import numpy as np
from scipy.optimize import minimize

class MarginCalibration:

    def __init__(self,
                sampling_probabilities,
                calibration_matrix,
                calibration_target,
                calibration_method):
        
        self.sampling_probabilities = sampling_probabilities
        self.calibration_matrix = calibration_matrix
        self.calibration_target = calibration_target
        self.calibration_method = calibration_method

    def initialize_sampling_weights(self):
        return np.array([1/prob_i for prob_i in self.sampling_probabilities])

    def _linear_method(self, w, d):
        return ((w/d-1)**2)

    def _ranking_ratio_method(self, w, d):
        return (w/d)*np.log(w/d)-(w/d)+1

    # def _logit_method(self, w, d, lower_bound, upper_bound):
    #     pass
        
    def initialize_method(self):
        
        dict_method = {
            "linear":self._linear_method,
            "ranking_ratio":self._ranking_ratio_method
        }
        try:
            return dict_method[self.calibration_method]

        except:
            raise ValueError(f"Invalid value : {self.calibration_method}. Must be one of : 'linear', 'ranking_ratio'")

    def objective(self, calibration_weights):
        
        sampling_weights = self.initialize_sampling_weights()
        
        return sum(
            d_k*self.initialize_method()(w_k, d_k) for w_k, d_k in zip(calibration_weights, 
                                                                      sampling_weights)
        )

    def constraint(self, calibration_weights):
        return self.calibration_matrix.T@calibration_weights-self.calibration_target

    def calibration(self):
        
        constraints = {"type":"eq", "fun":self.constraint}
        
        x0 = self.initialize_sampling_weights()
        
        return minimize(
            self.objective,
            x0=x0,
            method = "trust-constr",
            constraints = constraints
        )    