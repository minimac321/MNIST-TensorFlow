from keras.datasets import mnist
from sklearn.model_selection import train_test_split

from src.feedforward_network import FeedForwardNeuralNetwork
from src.neural_network_utils import transform_mnist_x_data, plot_loss_curve, plot_accuracy_curve


def load_mnist_data(train_validation_split: float = 0.25, verbose: bool = True):
    """ Load MNIST data and split into training, test and validation sets """
    # Load data
    (x_train_initial, y_train_initial), (x_test_mnist, y_test_mnist) = mnist.load_data()
    total_rows = len(x_train_initial) + len(x_test_mnist)

    if verbose:
        print(f"MNIST dataset size = {total_rows}")
        print(f"x_train.shape: {x_train_initial.shape}, y_train.shape: {y_train_initial.shape}")
        print(
            f"x_test_mnist.shape:  {x_test_mnist.shape},  y_test_mnist.shape: {y_test_mnist.shape}")

    # 2. Create validation set from training set
    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_initial,
        y_train_initial, test_size=train_validation_split,
        random_state=8
    )  # 0.25 x 0.8 = 0.2

    # Transform x values
    x_train = transform_mnist_x_data(x_train)
    x_validation = transform_mnist_x_data(x_validation)
    x_test_mnist = transform_mnist_x_data(x_test_mnist)

    if verbose:
        print(f"X_train shape: {x_train.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"X_val shape: {x_validation.shape}")
        print(f"y val shape: {y_validation.shape}")
        print(f"x_test_mnist shape: {x_test_mnist.shape}")
        print(f"y_test_mnist shape: {y_test_mnist.shape}")

    return x_train, y_train, x_validation, y_validation, x_test_mnist, y_test_mnist


def solve_mnist():
    x_train, y_train, x_validation, y_validation, x_test_mnist, y_test_mnist = load_mnist_data()

    # Set the number of epochs
    epochs = 100
    # Set the batch size
    batch_size = 256
    # Set the base learning rate
    learning_rate = 0.01
    # Number of inputs
    num_inputs = 28 * 28
    # Number of outputs
    num_outputs = 10
    # Size of hidden layer
    hidden_size = 250

    # data fitting, training and accuracy evaluation
    neural_net = FeedForwardNeuralNetwork(num_inputs, hidden_size, num_outputs)
    loss_function_dict, validation_dict = neural_net.train(
        x_train=x_train, y_train=y_train,
        x_valid=x_validation, y_valid=y_validation,
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate
    )
    accuracy = neural_net.testing(x_test=x_test_mnist, y_test=y_test_mnist)
    print(f"Accuracy: {accuracy:.3f}")

    plot_loss_curve(loss_function_dict)
    plot_accuracy_curve(validation_dict, final_test_accuracy=accuracy)


if __name__ == "__main__":
    solve_mnist()
