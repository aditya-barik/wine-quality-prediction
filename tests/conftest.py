import json
import pytest
import yaml

config_path = "params.yaml"
schema_path = r"wine_quality_prediction_service/schema/min_max_schema.json"


@pytest.fixture
def config(config_path=config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


@pytest.fixture
def schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema
