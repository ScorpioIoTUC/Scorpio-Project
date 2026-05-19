from threading import Lock
from typing import Optional

from decoder.libs.decoder_client import (
    DecoderClient,
    DecoderClientInitArgs,
    PreprocessDataArgs,
)


class Decoder:
    """Singleton facade for the decoder client.

    Supported config kwargs:
        samp_rate (int): SDR sample rate in samples/second. Default: 1_000_000.
        center_freq (float): RF center frequency in Hz. Default: 915_000_000.
        bw (int): LoRa bandwidth in Hz. Default: 250_000.
        sf (int): LoRa spreading factor. Default: 7.
        gain (int): SDR receiver gain. Default: 40.
        cr (int): LoRa coding rate denominator offset. Default: 1.
        has_crc (bool): Enable payload CRC verification. Default: True.
        impl_head (bool): Enable implicit header mode. Default: False.
        pay_len (int): Expected payload length (implicit header mode). Default: 64.
        sync_word (int): LoRa sync word. Default: 0x12.
        soft_decoding (bool): Enable soft decision decoding. Default: True.
        ldro_mode (int): Low Data Rate Optimization mode. Default: 2.
        print_rx (list[bool]): GNU Radio LoRa RX print flags. Default: [False, False].

    Notes:
        - The first instantiation applies the config.
        - Later instantiations return the same object and ignore new config.
        - Use `reset_instance()` to allow reconfiguration.
    """

    _instance: Optional["Decoder"] = None
    _lock = Lock()

    def __new__(cls, **config):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **config):
        """Create the singleton decoder using `DecoderClientInitArgs` kwargs.

        Args:
            **config: Decoder client initialization kwargs listed in the class
                docstring.
        """

        if getattr(self, "_initialized", False):
            return

        self._init_args = DecoderClientInitArgs(
            **config, client_name=config.get("client_name", "gnuradio_client")
        )
        self._client = DecoderClient(self._init_args)
        self._initialized = True

    @classmethod
    def create(cls, **config) -> "Decoder":
        return cls(**config)

    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            cls._instance = None

    @property
    def init_args(self) -> DecoderClientInitArgs:
        return self._init_args

    def start(self) -> None:
        self._client.start()

    def stop(self) -> None:
        self._client.stop()

    def get_total_messages(self) -> int:
        return self._client.get_total_messages()

    def get_message(self, index: int) -> object:
        return self._client.get_message(index)

    def preprocess_data(self, msg_pmt: object) -> str:
        """Preprocess a PMT message without requiring type imports by caller."""

        return self._client.preprocess_data(PreprocessDataArgs(msg_pmt=msg_pmt))
