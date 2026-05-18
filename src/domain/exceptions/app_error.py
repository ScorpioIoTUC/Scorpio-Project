from .error_codes import ErrorCode


class AppError(Exception):
    def __init__(self, error: ErrorCode, *, details: str = ""):
        self.error = error
        self.details = details

        super().__init__(self.__str__())

    def __str__(self):
        base = f"[{self.error.code}] {self.error.description}"
        return f"{base} - {self.details}" if self.details else base

    @classmethod
    def db_operation_failed(cls, details=""):
        return cls(ErrorCode.DB01, details=details)

    @classmethod
    def db_connection_failed(cls, details=""):
        return cls(ErrorCode.DB02, details=details)
    
    @classmethod
    def invalid_topic(cls, details=""):
        return cls(ErrorCode.VAL01, details=details)

    @classmethod
    def invalid_payload(cls, details=""):
        return cls(ErrorCode.VAL01, details=details)
    
    @classmethod
    def publish_error(cls, details=""):
        return cls(ErrorCode.PUB01, details=details)
    
    @classmethod
    def too_many_publish_errors(cls, details=""):
        return cls(ErrorCode.PUB02, details=details)
    
    @classmethod
    def cloud_send_error(cls, details=""):
        return cls(ErrorCode.CS01, details=details)    
    
    @classmethod
    def unidentified_satellite(cls, details=""):
        return cls(ErrorCode.PR01, details=details)
    
    @classmethod
    def deserialization_error(cls, details=""):
        return cls(ErrorCode.PR02, details=details)
    
    @classmethod
    def unknown_error(cls, details=""):
        return cls(ErrorCode.UNKNOWN, details=details)

    def to_dict(self):
        return {
            "error_code": self.error.code,
            "message": self.error.description,
            "details": self.details,
        }
