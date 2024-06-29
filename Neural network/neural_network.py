
from typing import Callable
import numpy as np
import numpy.typing as npt
from matplotlib import pyplot as plt


class NeuralNetwork:
    """
    Class to construct a neural network
    """

    # Activation functions
    sigmoid_activation_function    = lambda x: 1 / (1 + np.exp(-x))
    tanh_activation_function       = lambda x: np.tanh(x)
    relu_activation_function       = lambda x: np.maximum(0, x)
    leaky_relu_activation_function = lambda x, alpha = 0.05: np.where(x > 0, x, x * alpha)

    def __init__(self, network_size: list[int], activation_function: Callable = sigmoid_activation_function) -> None:
        self.network_size = network_size
        self.activation_function = activation_function
        self.values = [np.array([0 for _ in range(layer_size)]) for layer_size in network_size]  # List of all nodes structured into layers
        self.weights = [np.array([[np.random.uniform(-1, 1) for _ in range(layer_size)] for _ in range(network_size[i + 1])]) for i, layer_size in enumerate(network_size[:-1])]  # List of matrices of weights
        self.biases = [np.array([np.random.uniform(-1, 1) for _ in range(layer_size)]) for layer_size in network_size[1:]]
    
    def forward_propagation(self, input_values: npt.NDArray[np.float64]) -> None:
        assert(len(input_values) == self.network_size[0])  # To ensure input is of right size
        assert(type(input_values) == np.ndarray)           # To ensure correct typing for optimization
        assert all(abs(x) <= 1 for x in input_values)      # To ensure correct activation of input nodes

        self.values[0] = input_values
        for i, _ in enumerate(self.network_size[1:]):
            self.values[i + 1] = self.activation_function(np.matmul(self.weights[i], self.values[i]) + self.biases[i])
    
    @staticmethod
    def plot_activation_function(activation_function: Callable[[float], float], low: float = -10, high: float = 10, n: int = 1000) -> None:
        x_values = np.linspace(low, high, n)
        plt.plot(x_values, activation_function(x_values))
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    network_size = [5, 3, 2]
    neural_network = NeuralNetwork(network_size)
    print(network_size)
    print(neural_network.values)
    print(neural_network.weights)
    print(neural_network.biases)

    input_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    neural_network.forward_propagation(input_values)
    print(neural_network.values)
