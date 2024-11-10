import io
import os
from typing import List
from fastapi import FastAPI
import uvicorn
import logging
from dataset_params import (
    API_ATTR_EQUIPMENT_TYPE,
    API_ATTR_FAILURE_POINT,
    API_ATTR_SERIAL,
)
from dto import ApiRequest, ApiResponse, ClassifierAttributeDto
from server_params import (
    LocalServerMethod,
    LocalServerOptions,
    TEST_SERVER_ENDPOINT,
    TEST_SERVER_PORT,
)

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def version():
    return {"version": "1.0.0"}


@app.post(TEST_SERVER_ENDPOINT)
async def classify(request: ApiRequest) -> ApiResponse:
    options = LocalServerOptions.model_validate(request.options)
    attributes: List[ClassifierAttributeDto]
    if options.method == LocalServerMethod.CONSTANT:
        attributes = [
            ClassifierAttributeDto(name=API_ATTR_EQUIPMENT_TYPE, value="Сервер"),
            ClassifierAttributeDto(
                name=API_ATTR_FAILURE_POINT, value="Материнская плата"
            ),
            ClassifierAttributeDto(name=API_ATTR_SERIAL, value="12345"),
        ]
    elif options.method == LocalServerMethod.EMPTY:
        attributes = []
    else:
        raise Exception(f"Unknown method {options.method}")

    return ApiResponse(attributes=attributes)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=TEST_SERVER_PORT,
        reload=False,
        log_level="debug",
    )
