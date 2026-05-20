from gnuradio import blocks, gr, soapy  # type: ignore[import-not-found]
import gnuradio.lora_sdr as lora_sdr  # type: ignore[import-not-found]
import pmt  # type: ignore[import-not-found]

from decoder.libs.decoder_client.decoder_client_contract import DecoderClientContract
from decoder.libs.decoder_client.types.decoder_client_types import DecoderClientInitArgs, PreprocessDataArgs


class _LoraRxTopBlock(gr.top_block):
    def __init__(self, args: DecoderClientInitArgs):
        super().__init__("My LoRa Receiver")

        self.src = soapy.source("driver=rtlsdr", "fc32", 1, "", "", [""], [""])
        self.src.set_sample_rate(0, args.samp_rate)
        self.src.set_frequency(0, args.center_freq)
        self.src.set_gain_mode(0, False)
        self.src.set_gain(0, args.gain)

        self.lora_rx = lora_sdr.lora_sdr_lora_rx(
            bw=args.bw,
            cr=args.cr,
            has_crc=args.has_crc,
            impl_head=args.impl_head,
            pay_len=args.pay_len,
            samp_rate=args.samp_rate,
            sf=args.sf,
            sync_word=[args.sync_word],
            soft_decoding=args.soft_decoding,
            ldro_mode=args.ldro_mode,
            print_rx=args.print_rx,
        )

        self.msg_debug = blocks.message_debug()

        self.connect((self.src, 0), (self.lora_rx, 0))
        self.msg_connect((self.lora_rx, "out"), (self.msg_debug, "store"))


class GnuRadioClient(DecoderClientContract):
    def __init__(self, args: DecoderClientInitArgs):
        self._tb = _LoraRxTopBlock(args)

    def start(self) -> None:
        self._tb.start()

    def stop(self) -> None:
        self._tb.stop()
        self._tb.wait()

    def preprocess_data(self, args: PreprocessDataArgs) -> str:
        msg_pmt = args.msg_pmt
        if pmt.is_pair(msg_pmt):
            data_part = pmt.cdr(msg_pmt)
        else:
            data_part = msg_pmt

        payload = pmt.to_python(data_part)

        if isinstance(payload, (bytes, list)):
            return "".join(chr(b) for b in payload if 32 <= b <= 126)
        return str(payload)

    def get_total_messages(self) -> int:
        return self._tb.msg_debug.num_messages()

    def get_message(self, index: int) -> object:
        return self._tb.msg_debug.get_message(index)
