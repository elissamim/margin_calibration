import numpy as np
import pandas as pd
from scipy.optimize import minimize
from utils import (
                    check_nans,
                    check_zeros,
                    check_negative_values
                  )

class MarginCalibration:
    """
    A class for calibrating weights based on different calibration methods.

    The class provides methods for weight calibration based on linear,
    raking ratio, truncated linear, or logit methods, with options for 
    penalty and cost constraints. The calibration process involves 
    optimizing an objective function to match sampling probabilities to 
    a calibration target.

    Attributes:
        calibration_method (str): The calibration method to use. Must be one of 
                                  'linear', 'raking_ratio', 'truncated_linear', or 'logit'.
        lower_bound (float or None): The lower bound for methods like 'logit'.
        upper_bound (float or None): The upper bound for methods like 'logit'.
        penalty (float or None): The penalty parameter for cost-based optimization.
        costs (array-like or None): The cost associated with the calibration.
    """

    def __init__(
        self,
        calibration_method="linear",
        lower_bound=None,
        upper_bound=None,
        penalty=None,
        costs=None,
    ):
        """
        Initializes the MarginCalibration object.

        Args:
            calibration_method (str): The calibration method to use ('linear', 'raking_ratio', 'truncated_linear', 'logit').
            lower_bound (float or None): The lower bound for calibration methods requiring it (e.g., 'logit').
            upper_bound (float or None): The upper bound for calibration methods requiring it (e.g., 'logit').
            penalty (float or None): Penalty for cost-based optimization.
            costs (array-like or None): The cost matrix to be used in optimization.
        """
        self.calibration_method = calibration_method
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.penalty = penalty
        self.costs = costs

    def _to_numpy(self, data: pd.DataFrame) -> np.ndarray:
        """
        Converts input data to a NumPy array.

        Args:
            data (pd.DataFrame, pd.Series, or np.ndarray): The data to convert.

        Returns:
            np.ndarray: The converted data.

        Raises:
            TypeError: If the input data is not a DataFrame, Series, or ndarray.
        """
        if isinstance(data, pd.DataFrame):
            if data.shape[1] == 1:
                return data.to_numpy().flatten()
            else:
                return data.to_numpy()
        elif isinstance(data, pd.Series):
            return data.to_numpy()
        elif isinstance(data, np.ndarray):
            return data
        else:
            raise TypeError(
                """Input must be a NumPy array or Pandas DataFrame/Series."""
            )

    def _initialize_sampling_weights(self):
        """
        Initializes the sampling weights based on the sampling probabilities.

        Returns:
            np.ndarray: The initialized sampling weights.
        """
        return 1 / self.sampling_probabilities

    def _linear_method(self, w, d):
        """
        Linear method for calibration.

        Args:
            w (float): The weight.
            d (float): The distance.

        Returns:
            float: The computed value based on the linear method.
        """
        return (w / d - 1) ** 2

    def _raking_ratio_method(self, w, d):
        """
        Raking ratio method for calibration.

        Args:
            w (float): The weight.
            d (float): The distance.

        Returns:
            float: The computed value based on the raking ratio method.
        """
        epsilon=1e-8
        return (w / d) * np.log(np.maximum(w / d, epsilon)) - (w / d) + 1

    def _logit_method(self, w, d):
        """
        Logit method for calibration.

        Args:
            w (float): The weight.
            d (float): The distance.

        Returns:
            float: The computed value based on the logit method.
        """
        epsilon = 1e-8
        x = w / d
        a = (x - self.lower_bound) * np.log(
            np.maximum((x - self.lower_bound) / (1 - self.lower_bound), epsilon)
        )
        b = (self.upper_bound - x) * np.log(
            np.maximum((self.upper_bound - x) / (self.upper_bound - 1), epsilon)
        )
        c = (self.upper_bound - self.lower_bound) / (
            (1 - self.lower_bound) * (self.upper_bound - 1)
        )
        return (a + b) / c

    def _initialize_method(self):
        """
        Initializes the appropriate method based on the chosen calibration method.

        Returns:
            function: The method to use for calibration (e.g., linear, raking_ratio, logit).
        
        Raises:
            ValueError: If an invalid calibration method is provided.
        """
        dict_method = {
            "linear": self._linear_method,
            "raking_ratio": self._raking_ratio_method,
            "truncated_linear": self._linear_method,
            "logit": self._logit_method,
        }
        try:
            return dict_method[self.calibration_method]
        except KeyError:
            raise ValueError(
                f"""Invalid value : {self.calibration_method}. 
                Must be one of : 'linear', 'raking_ratio', 'truncated_linear'"""
            )

    def _compute_jacobian(self, calibration_weights):
        """
        Computes the Jacobian (or rather gradient) for the different methods, 
        to make optimization faster.

        Args:
            calibration_weights (np.ndarray): The calibration weights.

        Returns:
            np.ndarray: The gradient for a given method.
        """

        epsilon=1e-8
        
        if self.calibration_method in ["linear", "truncated_linear"]:
            gradient = calibration_weights/self._initialize_sampling_weights()-1
        elif self.calibration_method == "raking_ratio":
            gradient = np.log(np.maximum(calibration_weights/self._initialize_sampling_weights(), 
                            epsilon))
        elif self.calibration_method == "logit":
            a = (self.upper_bound - self.lower_bound)/((1 - self.lower_bound)*(self.upper_bound - 1))
            r = calibration_weights/self._initialize_sampling_weights()
            gradient =  1/a * np.log(np.maximum(coeff_2*(r - self.lower_bound)/(self.upper_bound - r),
                                            epsilon))
        else:
            raise ValueError("""
                            Gradient computed for 'linear', 'raking_ratio', 'logit', and 'truncated_linear'
                            distances.
                            """)

        if (self.penalty is None) and (self.costs is None):
            return gradient
        elif (self.penalty is not None) and (self.costs is not None):
            penalty_gradient =
            return gradient + penalty_gradient
        else:
            raise ValueError(
                """Both 'penalty' and 'costs' must be given, 
                            in case one is given."""
            )

    def _objective(self, calibration_weights):
        """
        Computes the objective function to minimize during calibration.

        Args:
            calibration_weights (np.ndarray): The calibration weights.

        Returns:
            float: The value of the objective function (sum of distances, possibly with penalty).
        
        Raises:
            ValueError: If only one of 'penalty' or 'costs' is provided.
        """
        if (self.penalty is None) and (self.costs is None):

            sampling_weights = self._initialize_sampling_weights()

            return sum(
                d_k * self._initialize_method()(w_k, d_k)
                for w_k, d_k in zip(calibration_weights, sampling_weights)
            )

        elif (self.penalty is not None) and (self.costs is not None):

            sampling_weights = self._initialize_sampling_weights()
            total_target = self.calibration_target

            distance = sum(
                d_k * self._initialize_method()(w_k, d_k)
                for w_k, d_k in zip(calibration_weights, sampling_weights)
            )

            margin_gap = self.calibration_matrix.T @ calibration_weights - total_target

            cost = self.penalty * np.dot(margin_gap, np.diag(self.costs) @ margin_gap)

            return distance + cost

        else:

            raise ValueError(
                """Both 'penalty' and 'costs' must be given, 
                            in case one is given."""
            )

    def _constraint(self, calibration_weights):
        """
        Defines the constraint for the optimization problem.

        Args:
            calibration_weights (np.ndarray): The calibration weights.

        Returns:
            np.ndarray: The result of the constraint (calibration matrix times weights minus the target).
        """
        return self.calibration_matrix.T @ calibration_weights - self.calibration_target

    def calibration(
        self, sampling_probabilities, calibration_matrix, calibration_target
    ):
        """
        Performs the calibration optimization process.

        Args:
            sampling_probabilities (array-like): The sampling probabilities.
            calibration_matrix (array-like): The calibration matrix.
            calibration_target (array-like): The target values for calibration.

        Returns:
            OptimizeResult: The result of the optimization process.
        
        Raises:
            ValueError: If NaNs found in the sampling probabilities vector.
            ValueError: If 0 values found in the sampling probabilities vector.
            ValueError: If negative values found in the sampling probabilities vector.
            ValueError: If the lower bound is not strictly less than 1, or the upper bound is not strictly greater than 1 for methods like 'logit'.
            TypeError: If bounds are not numeric values when using methods like 'logit'.
        """
        # Store the passed values as instance variables
        self.sampling_probabilities = self._to_numpy(sampling_probabilities)
        self.calibration_matrix = self._to_numpy(calibration_matrix)
        self.calibration_target = self._to_numpy(calibration_target)

        # Apply basic checks on weights and calibration data
        check_nans(self.sampling_probabilities,
                  """
                  NaN values found in sampling probabilities.
                  """)
        check_zeros(self.sampling_probabilities,
                   """
                   Zero values found in sampling probabilities.
                   """)
        check_negative_values(self.sampling_probabilities,
                             """
                             Negative values found in sampling probabilities.
                             """)

        # Check for NaNs in calibration variables
        check_nans(self.calibration_matrix,
                  """
                  NaN values found in calibration matrix.
                  """)
        
        # Check for NaNs in total margins
        check_nans(self.calibration_target,
                  """
                  NaN values found in calibration target.
                  """)
        
        # Define the constraints for constrained problems
        if (self.penalty is None) and (self.costs is None):
            constraints = {"type": "eq", "fun": self._constraint}
        elif (self.penalty is not None) and (self.costs is not None):
            constraints = None
        else:
            raise ValueError(
                """Both 'penalty' and 'costs' must be given, 
                            in case one is given."""
            )

        x0 = self._initialize_sampling_weights()

        if self.calibration_method in ["truncated_linear", "logit"]:
            if isinstance(self.lower_bound, (int, float)) and isinstance(
                self.upper_bound, (int, float)
            ):
                if (self.lower_bound < 1) and (self.upper_bound > 1):
                    sampling_weights = self._initialize_sampling_weights()
                    bounds = [
                        (self.lower_bound * d_k, self.upper_bound * d_k)
                        for d_k in sampling_weights
                    ]
                else:
                    raise ValueError(
                        """The lower bound should be strictly inferior to 1, 
                        the upper bound strictly superior to 1"""
                    )
            else:
                raise TypeError(
                    """'lower_bound' and 'upper_bound' must be numeric values
                    when using 'truncated_linear' or 'logit' methods"""
                )
        elif self.calibration_method == "raking_ratio":
            sampling_weights = self._initialize_sampling_weights()
            bounds = [
                (0, None)
                for d_k in sampling_weights
            ]
        else:
            bounds = None

        return minimize(
            self._objective,
            x0=x0,
            method="trust-constr",
            constraints=constraints,
            bounds=bounds,
            jac=self._compute_jacobian
        )