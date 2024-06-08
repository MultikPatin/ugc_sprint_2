from abc import ABC, abstractmethod


class BaseBrokerProducer(ABC):
    @abstractmethod
    def produce(self, *args, **kwargs):
        raise NotImplementedError
