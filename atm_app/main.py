import os
from src.app import create_app
from src.config import get_config


config_env = os.getenv("ENV", "development")
app_config = get_config(config_env)

flask_app = create_app(app_config)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=True)