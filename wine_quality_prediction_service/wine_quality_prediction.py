import joblib
import json
import os

import numpy as np

from src.utils import load_config

config_path = "params.yaml"
schema_path = os.path.join(
    os.path.dirname(__file__),
    "schema",
    "min_max_schema.json"
)


class NotInRangeError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class NotInColumnsError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def load_schema(schema_path=schema_path):
    with open(schema_path, "r") as json_file:
        schema = json.load(json_file)
    return schema


def is_valid_input(request_dict):
    schema = load_schema(schema_path)

    def _is_valid_col_name(col):
        if col not in schema.keys():
            raise NotInColumnsError(f"{col} is not a valid column")

    def _is_valid_col_value(col, val):
        min_valid_val = schema[col]["min"]
        max_valid_val = schema[col]["max"]
        if not min_valid_val <= float(val) <= max_valid_val:
            raise NotInRangeError(
                f"For {col} column, "
                f"{val} is not in valid range. "
                f"Valid Range is: [{min_valid_val}, {max_valid_val}]"
            )
    for col, val in request_dict.items():
        _is_valid_col_name(col)
        _is_valid_col_value(col, val)

    return True


def predict(data):
    config = load_config(config_path=config_path)
    schema = load_schema(schema_path=schema_path)
    model = joblib.load(
        os.path.join(config["web_app_model_dir"], "model.joblib")
    )
    prediction = model.predict(data)[0]
    print("prediction : ", prediction)

    try:
        pred_min_val = schema[config["base"]["target_col"]]["min"]
        pred_max_val = schema[config["base"]["target_col"]]["max"]
        if pred_min_val <= prediction <= pred_max_val:
            return prediction
        else:
            raise NotInRangeError(
                "Predicted value is not in valid range of [3, 8]"
            )
    except NotInRangeError:
        return "Predicted value is not in valid range of [3, 8]"


def get_web_response(request_dict):
    if is_valid_input(request_dict):
        data = [list(map(float, request_dict.values()))]
        response = predict(data)
        return response


def get_api_response(request_dict):
    try:
        if is_valid_input(request_dict):
            data = np.array([list(request_dict.values())])
            response = {
                "response": predict(data)
            }
        else:
            response = {
                "response": None,
                "valid_range": load_schema()
            }
    except NotInColumnsError as e:
        response = {
            "response": str(e),
            "valid_columns": list(load_schema().keys())
        }
    except NotInRangeError as e:
        response = {
            "response": str(e),
            "valid_range": load_schema()
        }
    except Exception as e:
        response = {
            "response": str(e)
        }
    finally:
        return response
