import logging
import os
from typing import List, cast
from numpy import average
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from server_params import evaluating_methods

from dataset_params import (
    DS_ATTR_EQUIPMENT_TYPE,
    DS_ATTR_FAILURE_POINT,
    DS_ATTR_ID,
    DS_ATTR_MESSAGE,
    DS_ATTR_SERIAL,
    DS_ATTR_TOPIC,
    ds_train_file,
    ds_predict_file,
    ds_scores_file,
    ds_attrs,
    api_attrs,
)
from utils import file_exists, pandas_append

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


metrics_rules = {
    "et_wf1": (
        DS_ATTR_EQUIPMENT_TYPE,
        lambda y_true, y_pred: f1_score(
            y_true=y_true,
            y_pred=y_pred,
            average="weighted",
            zero_division=cast(str, 0.0),
        ),
    ),
    "fp_wf1": (
        DS_ATTR_FAILURE_POINT,
        lambda y_true, y_pred: f1_score(
            y_true=y_true,
            y_pred=y_pred,
            average="weighted",
            zero_division=cast(str, 0.0),
        ),
    ),
    "sn_accuracy": (
        DS_ATTR_SERIAL,
        lambda y_true, y_pred: accuracy_score(y_true=y_true, y_pred=y_pred),
    ),
}


def main():
    df_train = pd.read_csv(ds_train_file, index_col=DS_ATTR_ID)
    IDX_LABEL = "#"
    df_map = (
        {"method": []} | {m_rule: [] for m_rule in metrics_rules.keys()} | {"score": []}
    )

    for method in evaluating_methods:
        name = method.name
        predict_file = ds_predict_file.format(name=name)
        if not file_exists(predict_file):
            continue
        df_pred = pd.read_csv(predict_file, index_col=DS_ATTR_ID)
        df_merged = pd.merge(
            df_train,
            df_pred,
            suffixes=("_true", "_pred"),
            left_index=True,
            right_index=True,
        )
        df_merged.fillna("", inplace=True)

        df_map["method"].append(name)
        score_parts: List[float] = []
        for m_rule, (attr_name, score_fn) in metrics_rules.items():
            score_val = score_fn(
                y_true=df_merged[attr_name + "_true"],
                y_pred=df_merged[attr_name + "_pred"],
            )
            score_parts.append(score_val)
            df_map[m_rule].append(score_val)
        df_map["score"].append(average(score_parts))

    df_score = pd.DataFrame(df_map)
    df_score.to_csv(ds_scores_file, index_label=IDX_LABEL)

    print(f"\n\n{df_score.to_markdown()}")
    

if __name__ == "__main__":
    main()
