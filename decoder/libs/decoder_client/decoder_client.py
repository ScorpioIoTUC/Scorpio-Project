from .decoder_client_contract import DecoderClientContract
from .types.decoder_client_types import DecoderClientInitArgs, PreprocessDataArgs
from .clients.gnu_radio.gnuradio_client import GnuRadioClient

class DecoderClient(DecoderClientContract):
    CLIENTS = {"gnuradio_client"}

    def __init__(self, args: DecoderClientInitArgs) -> None:
        if args.client_name not in DecoderClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)
        if args.client_name == "gnuradio_client":
            self.client_obj = GnuRadioClient(args)
        self.client_name = args.client_name

    def start(self) -> None:
        return self.client_obj.start()

    def stop(self) -> None:
        return self.client_obj.stop()

    def preprocess_data(self, args: PreprocessDataArgs) -> str:
        return self.client_obj.preprocess_data(args)

    def get_total_messages(self) -> int:
        return self.client_obj.get_total_messages()

    def get_message(self, index: int) -> object:
        return self.client_obj.get_message(index)
