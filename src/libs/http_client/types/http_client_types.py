from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class HTTPClientInitArgs:
    client_name: str
    credentials: Optional[Dict[str, Any]] = None


@dataclass
class HTTPRequestArgs:
    url: str
    headers: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None
    json: Optional[Any] = None
    timeout: Optional[float] = None