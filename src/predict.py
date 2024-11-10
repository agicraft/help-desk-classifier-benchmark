import logging
import os
from typing import Any, Dict, cast
import httpx
import pandas as pd
from sklearn.metrics import f1_score
from dto import ApiRequest, ApiResponse
from server_params import (
    evaluating_methods,
    EvalMethod,
)
import time

from dataset_params import (
    DS_ATTR_ID,
    DS_ATTR_MESSAGE,
    DS_ATTR_TOPIC,
    ds_train_file,
    ds_predict_file,
    ds_attrs,
    api_attrs,
)
from utils import file_exists, pandas_append

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


def main():
    df_train = pd.read_csv(ds_train_file, index_col=DS_ATTR_ID)
    df_predict_by_method: Dict[str, pd.DataFrame] = {}

    api2ds_attr_map: Dict[str, str] = {
        api_attr: ds_attr for api_attr, ds_attr in zip(api_attrs, ds_attrs)
    }

    for idx, row in df_train.iterrows():
        message = str(row[DS_ATTR_MESSAGE])
        topic = str(row[DS_ATTR_TOPIC])

        for method in evaluating_methods:
            name = method.name
            predict_file = ds_predict_file.format(name=name)
            if name not in df_predict_by_method:
                if file_exists(predict_file):
                    df_predict_by_method[name] = pd.read_csv(
                        predict_file, index_col=DS_ATTR_ID
                    )
                else:
                    df_predict_by_method[name] = pd.DataFrame(
                        columns=cast(Any, [DS_ATTR_TOPIC, DS_ATTR_MESSAGE] + ds_attrs)
                    )

            df_predict = df_predict_by_method[name]

            if idx in df_predict.index:
                logger.info(f"Row #{idx=} {name=} skipping")
                continue
            logger.info(f"Row #{idx=} {name=} PREDICTING")

            response = do_client_request(method=method, message=message, topic=topic)
            df_predict = pandas_append(
                df_predict,
                {
                    DS_ATTR_TOPIC: topic,
                    DS_ATTR_MESSAGE: message,
                }
                | {
                    api2ds_attr_map[attr.name]: attr.value
                    for attr in response.attributes
                },
                idx=idx,
            )
            df_predict_by_method[name] = df_predict

            # save after each iteration
            df_predict.to_csv(predict_file, index_label=DS_ATTR_ID)


def do_client_request(method: EvalMethod, message: str, topic: str):
    retry_timeout = 3
    retry_attempts = 10
    http_client = httpx.Client()
    for _ in range(retry_attempts):
        try:
            r = http_client.post(
                method.endpoint,
                json=ApiRequest(
                    text=message, topic=topic, options=method.options
                ).model_dump(mode="json"),
                timeout=120,
            )
            if not httpx.codes.is_success(r.status_code):
                logger.error(f"Request failed ({r.status_code}): {r.text}")
            else:
                return ApiResponse.model_validate_json(r.text)
        except KeyboardInterrupt:
            raise
        except:
            logger.exception("Request failed")
        logger.error(f"Retrying in {retry_timeout}s")
        time.sleep(retry_timeout)
    raise RuntimeError("All attempts failed")


if __name__ == "__main__":
    main()
