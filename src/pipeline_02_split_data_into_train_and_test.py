import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

from utils import load_config, watchit

@watchit
def load_data_from_local_source(local_data_source: str) -> pd.DataFrame:
    """load data from local source"""

    return pd.read_csv(
        local_data_source,
        sep = ",",
        encoding = "utf-8"
    )

@watchit
def split_and_save_data(
    data: pd.DataFrame,
    test_size: float,
    random_state: int,
    train_data_path: str,
    test_data_path: str
) -> None:
    """split data into train and test and save"""

    train_data, test_data = train_test_split(
        data,
        test_size = test_size,
        random_state = random_state
    )

    train_data.to_csv(
        train_data_path,
        sep = ",",
        index = False
    )
    test_data.to_csv(
        test_data_path,
        sep = ",",
        index = False
    )

def split_data_into_train_and_test_and_save(config_path: str) -> None:
    """split data into train and test and save"""

    config = load_config(config_path = config_path)

    raw_data = load_data_from_local_source(
        local_data_source = config["data_source"]["local_source"]
    )
    split_and_save_data(
        data = raw_data,
        test_size = config["split_data"]["test_size"],
        random_state = config["base"]["random_state"],
        train_data_path = config["split_data"]["train_data"],
        test_data_path = config["split_data"]["test_data"]
    )

if __name__=="__main__":

    parser = argparse.ArgumentParser(
        description = "Pipeline 02 - Split data into train and test and save"
    )
    parser.add_argument(
        "--config",
        required = True
    )
    args = parser.parse_args()

    split_data_into_train_and_test_and_save(config_path = args.config)
