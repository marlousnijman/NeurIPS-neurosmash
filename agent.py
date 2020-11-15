import mxnet as mx
from mxnet import nd
import numpy as np

import utils as u


class Agent(object):
    """
    Agent superclass
    """
    def step(self, reward, state):
        raise NotImplementedError


class RandomAgent(Agent):
    """

    """
    def __init__(self):
        pass

    def step(self, reward, state):
        return 3


class SimpleESAgent(Agent):
    """
    Simple agent that always takes the best action
    The evolutionary strategy (ES) perturbs its weight after each episode
    """
    def __init__(self, model, mean=0, sigma=0.05, ctx=mx.cpu()):
        self.model = model
        self.model.initialize(ctx=ctx)
        # Parameters for Gaussian noise
        self.mean = mean
        self.sigma = sigma

    def step(self, reward, state):
        actions_probabilities = self.model(nd.array(state)).asnumpy()
        return np.argmax(actions_probabilities)

    def perturb_weights(self):
        for layer in self.model.net:
            # Collect current layer weights
            cur_weights = u.get_weights(layer)

            # Sample gaussian noise with same shape as layer
            layer_shape = cur_weights.shape
            gaussian_noise = nd.random_normal(self.mean, self.sigma, shape=layer_shape)

            # Add gaussian noise to current weights to retrieve new weights
            new_weights = cur_weights + gaussian_noise
            # print(new_weights - cur_weights)
            # Force re-initialization of layer weights
            u.initialize_weights(layer, new_weights)