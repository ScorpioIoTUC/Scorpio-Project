from abc import ABC, abstractmethod

from .types.decoder_client_types import PreprocessDataArgs


class DecoderClientContract(ABC):
    @abstractmethod
    def start(self) -> None:
        """
        Start the decoder client. This method should initialize any necessary resources and begin processing data.
        """

        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the decoder client. This method should release any resources and halt data processing.
        """
        pass

    @abstractmethod
    def preprocess_data(self, args: PreprocessDataArgs) -> str:
        """
        Preprocess the raw data received from the decoder client. This method should take the raw
        data as input and return a human-readable string representation of the data.

        Args:
            args (PreprocessDataArgs): The arguments containing the raw data to preprocess.

        Returns:
            str: A human-readable string representation of the preprocessed data.
        """

        pass

    @abstractmethod
    def get_total_messages(self) -> int:
        """
        Get the total number of messages received.

        Returns:
            int: The total number of messages received.
        """
        pass

    @abstractmethod
    def get_message(self, index: int) -> object:
        """
        Get a specific message by its index.

        Args:
            index (int): The index of the message to retrieve.

        Returns:
            object: The requested message.
        """
        pass
