import numpy as np
import scipy.stats as stats


def generate_data(gen_params, n_samples, n_features, **kwargs):

    for dist_name, params in gen_params.items():
        
        dist = getattr(stats, dist_name)
        data = dist.rvs(size=[n_samples, n_features], **params)

    return np.sort(data, axis=0)


class DataGenerator():
    def __init__(self, mean=0.0, std=1.0, noise=False, is_int=False, x_dist='norm', y_dist='norm', is_nonlinear=False, nonlinear_func='sigmoid', seed=123, **kwargs) -> None:
    
        """
        Args:
        n_features (int): Number of features in the generated dataset.
        n_samples (int): Number of instances in the generated dataset.
        mean (float): The mean of the distribution.
        std (float): The standard deviation of the distribution (or scale parameter for exponential distribution).
        is_int (bool): Toggle to generate only integers instead of float numbers.
        x_dist (str): The distribution used for generating sample data. Choose one from ['norm', 'lognorm', 'uniform', 'expon', 'cauchy']
        y_dist (str): The distribution used for generating target data. Choose one from ['norm', 'lognorm', 'uniform', 'expon', 'cauchy']
        dist (str): The distribution used for generating data. Choose one from ['norm', 'lognorm', 'expon', 'cauchy']
        is_nonlinear (bool): Choice whether to apply non-linear transformation on the data.
        nonlinear_func (str): The non-linear transformation used to apply to the data.
        seed(int): Set the random seed.

        """
        self.mean = mean
        self.std = std
        self.noise = noise
        self.is_int = is_int
        self.x_dist = x_dist
        self.y_dist = y_dist
        self.is_nonlinear = is_nonlinear
        self.nonlinear_func = nonlinear_func
        self.seed = seed
        self.kwargs = kwargs

    def generate(self, n_features=10, n_samples=int(1e+4), **kwargs):

        """
        Funtion to generate the training data (both data samples and targets) from the chosen distribution with provided parameters.

        Args:
        n_features (int): Number of features in the generated dataset.
        n_samples (int): Number of instances in the generated dataset.
        """
        

        samp_dist = getattr(stats, self.x_dist)
        samples = samp_dist.rvs(size=(n_features, n_samples), **kwargs)

        targ_dist = getattr(stats, self.y_dist)
        target = targ_dist.rvs(size=n_samples, **kwargs)

        samples = np.sort(samples)
        target = np.sort(target)

        return (samples, target)


    def np_generate(self, n_features=10, n_samples=int(1e+4)):
        
        """
        Funtion to generate the training data (both data samples and targets) from the chosen distribution with provided parameters.

        Args:
        n_features (int): Number of features in the generated dataset.
        n_samples (int): Number of instances in the generated dataset.
        """

        np.random.seed(self.seed)

        # sampling from a chosen distribution 
        if self.dist == 'normal':
            samples = np.random.normal(self.mean, self.std, (n_samples, n_features))
        elif self.dist == 'lognormal':
            norm_samples = np.random.normal(self.mean, self.std, (n_samples, n_features))
            samples = np.exp(norm_samples)
            # samples = np.random.lognormal(self.mean, self.std, (n_samples, n_features))
        elif self.dist == 'uniform':
            samples = np.random.uniform(self.mean, self.std, (n_samples, n_features))
        elif self.dist == 'exponential':
            samples = np.random.exponential(self.std, (n_samples, n_features))
        else:
            raise ValueError('Invalid Distribution')

        # convert feature values to integer if specified
        if self.is_int:
            samples = np.round(samples).astype(int)

        # generating random weights
        weights = np.random.uniform(0, 1, n_features)

        # adding noise to the target is specified
        if self.noise:
            eps = np.random.normal(0, 1, n_samples)
        else:
            eps = 0

        # obtaining target dataset
        target = np.dot(samples, weights) + eps

        return (samples, target)


