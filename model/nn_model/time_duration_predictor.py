from abc import ABC, abstractmethod
from torch import Tensor
import torch.nn as nn
from torch import optim
from typing import Iterator

class TimeDurationPredictor(ABC):

    
    @abstractmethod
    def predict(self, X: Tensor) -> tuple[Tensor, Tensor]:
        """
        Predicts the minute of the day to turn on the lamp and the duration of the lamp usage in minutes.

        :param X: Tensor of shape (batch_size, 1) containing the input data.
        :type X: torch.Tensor
        :return: Tuple of two Tensors. The first Tensor contains the predicted time to turn on the lamp in minutes. The second Tensor contains the predicted duration of the lamp usage in minutes.
        :rtype: Tuple[torch.Tensor, torch.Tensor]
        """
        pass

    @abstractmethod
    def train(self, X: Tensor, y: Tensor, criterion: nn.Module, optimizer: optim.Optimizer, epochs: int) -> None:
        """
        Train the model on the input data.

        :param X: Tensor of shape (batch_size, 1) containing the input data.
        :type X: torch.Tensor
        :param y: Tensor of shape (batch_size, 2) containing the target data. The first column contains the time to turn on the lamp in minutes. The second column contains the duration of the lamp usage in minutes.
        :type y: torch.Tensor
        :param criterion: Loss function to use for training.
        :type criterion: torch.nn.Module
        :param optimizer: Optimizer to use for training.
        :type optimizer: torch.optim.Optimizer
        :param epochs: Number of epochs to train the model.
        :type epochs: int
        :rtype: None
        """
        pass


    @abstractmethod
    def evaluate(self, X: Tensor, y: Tensor) -> dict[str, float]:
        """
        Evaluate the model on the input data.
        
        :param X: Tensor of shape (batch_size, 1) containing the input data.
        :type X: torch.Tensor
        :param y: Tensor of shape (batch_size, 2) containing the target data. The first column contains the time to turn on the lamp in minutes. The second column contains the duration of the lamp usage in minutes.
        :type y: torch.Tensor
        :return: Dictionary containing the evaluation metrics.
        :rtype: dict[str, Number]
        """
        pass

    @abstractmethod
    def parameters(self) -> Iterator[nn.Parameter]:
        """
        Returns the parameters of the model.

        :return: Iterator over the parameters of the model.
        :rtype: torch.nn.Parameter
        """
        pass