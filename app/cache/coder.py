import json
from typing import Any

from pydantic import BaseModel


class Coder:
    @staticmethod
    def encode(value: Any) -> bytes:
        raise NotImplementedError

    @staticmethod
    def decode(value: bytes) -> Any:
        raise NotImplementedError

class JsonCoder(Coder):
    @staticmethod
    def encode(value: Any) -> bytes:
        if isinstance(value, BaseModel):
            value = value.dict()
        elif hasattr(value, "__dict__"):
            value = {
                key: val
                for key, val in value.__dict__.items()
                if not key.startswith("_")
                and key != "_sa_instance_state"
            }
        return json.dumps(value).encode()

    @staticmethod
    def decode(value: bytes) -> Any:
        return json.loads(value.decode())
