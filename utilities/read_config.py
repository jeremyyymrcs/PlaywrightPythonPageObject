import json
import os

# Initialize the configuration reader
config_file_path = os.path.join("..//config.json")

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

# Read the JSON configuration file
with open(config_file_path, "r") as file:
    config = json.load(file)


class ReadConfig:

    @staticmethod
    def _get_config_value(section, key, default=None):
        """Helper method to fetch config values with error handling."""
        try:
            return config[section][key]
        except KeyError as e:
            print(f"Error: {e}")
            return default

    @staticmethod
    def get_simple_login_url():
        return ReadConfig._get_config_value("url", "mfa_login_link")

    @staticmethod
    def get_user_name():
        return ReadConfig._get_config_value("credentials", "user_name")

    @staticmethod
    def get_password():
        return ReadConfig._get_config_value("credentials", "pass_word")

    @staticmethod
    def get_wrong_password():
        return ReadConfig._get_config_value("credentials", "wrong_password")

    @staticmethod
    def get_secret_key():
        return ReadConfig._get_config_value("credentials", "secret_key")
