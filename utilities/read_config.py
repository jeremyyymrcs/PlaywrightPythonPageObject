import json
import os


class Config:
    """Handles test configurations."""

    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

    try:
        with open(CONFIG_PATH, "r") as f:
            config_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error loading config file: {e}")

    LOGIN_URL = config_data.get("url", {}).get("mfa_login_link", "")
    USERNAME = config_data.get("credentials", {}).get("user_name", "")
    PASSWORD = config_data.get("credentials", {}).get("pass_word", "")
    WRONG_PASSWORD = config_data.get("credentials", {}).get("wrong_password", "")
