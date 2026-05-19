from dataclasses import dataclass, field
from typing import List


@dataclass
class DecoderClientInitArgs:
    """Initialization arguments for the decoder client.

    Attributes:
        samp_rate: SDR sample rate in samples per second.
        center_freq: RF center frequency in Hz.
        bw: LoRa bandwidth in Hz.
        sf: LoRa spreading factor.
        gain: SDR receiver gain.
        cr: LoRa coding rate denominator offset.
        has_crc: Whether LoRa payload CRC checking is enabled.
        impl_head: Whether implicit header mode is enabled.
        pay_len: Expected payload length for implicit header mode.
        sync_word: LoRa sync word used to filter packets.
        soft_decoding: Whether soft decision decoding is enabled.
        ldro_mode: Low Data Rate Optimization mode.
        print_rx: GNU Radio LoRa RX print flags.
        client_name: Decoder backend to instantiate.
    """

    samp_rate: int = 1_000_000
    center_freq: float = 915_000_000
    bw: int = 250_000
    sf: int = 7
    gain: int = 40
    cr: int = 1
    has_crc: bool = True
    impl_head: bool = False
    pay_len: int = 64
    sync_word: int = 0x12
    soft_decoding: bool = True
    ldro_mode: int = 2
    print_rx: List[bool] = field(default_factory=lambda: [False, False])
    client_name: str = "gnuradio_client"


@dataclass
class PreprocessDataArgs:
    """Arguments for preprocessing a single GNU Radio message.

    Attributes:
        msg_pmt: Raw PMT object emitted by GNU Radio (typically from the
            lora_rx 'out' message port). It can be a PDU pair ``(meta, data)``
            or a direct blob/vector payload.
    """

    msg_pmt: object