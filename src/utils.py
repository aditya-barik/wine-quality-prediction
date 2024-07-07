import argparse
from functools import wraps
import time
import yaml

def watchit(func):
    """decorator function to print execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        days = int(elapsed_time // (3600 * 24))
        hours = int(elapsed_time % (3600 * 24) // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        if (days == 0) and (hours == 0) and (minutes == 0):
            elapsed_time_str = f"Time elapsed to {func.__doc__} : {elapsed_time:.5f} seconds"
        elif (days == 0) and (hours == 0):
            elapsed_time_str = f"Time elapsed to {func.__doc__} : {minutes} minutes {seconds} seconds"
        elif (days == 0):
            elapsed_time_str = f"Time elapsed to {func.__doc__} : {hours} hours {minutes} minutes {seconds} seconds"
        else:
            elapsed_time_str = f"Time elapsed to {func.__doc__} : {days} days, {hours} hours {minutes} minutes {seconds} seconds"

        elapsed_time_str = f"\033[93m{elapsed_time_str}\033[0m"

        print(elapsed_time_str)

        return result
    return wrapper

def load_config(config_path: str) -> dict:
    """load config"""

    with open(config_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = "Load config"
    )
    parser.add_argument(
        "--config",
        required = True
    )
    args = parser.parse_args()

    config = load_config(config_path = args.config)
    print("config : \n", config)
