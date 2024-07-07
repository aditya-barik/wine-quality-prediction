import argparse

import pandas as pd

from .utils import load_config, watchit


@watchit
def fetch_data_from_remote_source(remote_data_source: str) -> pd.DataFrame:
    """fetch data from remote source"""

    return pd.read_csv(
        remote_data_source,
        sep=",",
        encoding="utf-8"
    )


@watchit
def save_data(data: pd.DataFrame, local_data_source: str) -> None:
    """save remote data in local"""

    modified_col_names = [col.replace(" ", "_") for col in data.columns]
    data.to_csv(
        local_data_source,
        sep=",",
        encoding="utf-8",
        header=modified_col_names,
        index=False
    )


def get_data_from_remote_source_and_save(config_path: str) -> None:
    """get data from remote source and save it in local"""

    config = load_config(config_path=config_path)
    data = fetch_data_from_remote_source(
        remote_data_source=config["data_source"]["remote_source"]
    )
    save_data(
        data=data,
        local_data_source=config["data_source"]["local_source"]
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Get data from remote source and save it in local"
    )
    parser.add_argument(
        "--config",
        required=True
    )
    args = parser.parse_args()

    get_data_from_remote_source_and_save(config_path=args.config)
