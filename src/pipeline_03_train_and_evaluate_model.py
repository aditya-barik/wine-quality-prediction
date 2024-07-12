import argparse
import joblib
import json
import os
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from utils import load_config, watchit


@watchit
def train_and_evaluate_model(config_path: str) -> None:
    """train and evaluate model"""

    config = load_config(config_path=config_path)

    train_data_path = config["split_data"]["train_data"]
    test_data_path = config["split_data"]["test_data"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]

    target_col = config["base"]["target_col"]

    params_file = config["reports"]["params"]
    scores_file = config["reports"]["scores"]

    train = pd.read_csv(train_data_path, sep=",", encoding="utf-8")
    test = pd.read_csv(test_data_path, sep=",", encoding="utf-8")

    x_train = train.drop([target_col], axis=1)
    y_train = train[[target_col]]

    x_test = test.drop([target_col], axis=1)
    y_test = test[target_col]

    model = ElasticNet(
        alpha=alpha,
        l1_ratio=l1_ratio,
        random_state=random_state
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    rmse, mae, r2 = calc_model_eval_metrics(obs=y_test.values, pred=y_pred)

    with open(params_file, "w") as f:
        params = {
            "alpha": alpha,
            "l1_ratio": l1_ratio
        }
        json.dump(params, f, indent=4)

    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(model, model_path)


def calc_model_eval_metrics(
    obs: np.ndarray,
    pred: np.ndarray
) -> Tuple[float, float, float]:
    """calculate model evalution metrics"""

    rmse = np.sqrt(mean_squared_error(obs, pred))
    mae = mean_absolute_error(obs, pred)
    r2 = r2_score(obs, pred)

    return rmse, mae, r2        # type: ignore


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Pipeline 03 - Train and evaluate model"
    )
    parser.add_argument(
        "--config",
        required=True
    )
    args = parser.parse_args()

    train_and_evaluate_model(config_path=args.config)
