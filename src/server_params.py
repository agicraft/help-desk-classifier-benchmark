from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict
from dataclasses import dataclass

TEST_SERVER_ENDPOINT = "/classify"
TEST_SERVER_PORT = 1234


class LocalServerMethod(Enum):
    CONSTANT = "constant"
    EMPTY = "empty"


class LocalServerOptions(BaseModel):
    method: LocalServerMethod


@dataclass
class EvalMethod:
    name: str
    endpoint: str
    options: Dict[str, Any]


test_server_url = f"http://localhost:{TEST_SERVER_PORT}{TEST_SERVER_ENDPOINT}"
local_server_url = "http://localhost:8080/api/classifier/classify"

evaluating_methods = [
    EvalMethod(
        name=LocalServerMethod.EMPTY.value,
        endpoint=test_server_url,
        options=LocalServerOptions(method=LocalServerMethod.EMPTY).model_dump(),
    ),
    EvalMethod(
        name=LocalServerMethod.CONSTANT.value,
        endpoint=test_server_url,
        options=LocalServerOptions(method=LocalServerMethod.CONSTANT).model_dump(),
    ),
    EvalMethod(
        name="baseline_llama31_8b",
        endpoint=local_server_url,
        options={},
    ),
]
