from abc import ABC, abstractmethod
from typing import List, Dict


class BaseDataset(ABC):
    """
    Base class for all datasets used in the evaluation framework.

    Every dataset adapter should inherit from this class and implement
    the load() method. The load() method should return a list of samples
    in a common format that can later be used by the model runner and evaluator.
    """

    @abstractmethod
    def load(self) -> List[Dict]:
        """
        Load dataset samples and return them as a list of dictionaries.

        Returns:
            List[Dict]: A list of standardized dataset samples.
        """
        raise NotImplementedError