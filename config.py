# config.py

import os
import yaml
import logging

logger = logging.getLogger(__name__)


def load_config():
    """
    Load configuration from the YAML file specified by CONFIG_PATH
    environment variable or the default path.
    """
    CONFIG_PATH = os.getenv("CONFIG_PATH", "config.yaml")

    if not os.path.exists(CONFIG_PATH):
        logger.error(f"Configuration file '{CONFIG_PATH}' not found.")
        raise FileNotFoundError(f"Configuration file '{CONFIG_PATH}' not found.")

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f) or {}
            logger.info(f"Configuration loaded successfully from '{CONFIG_PATH}'.")
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{CONFIG_PATH}': {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        raise


# Load the configuration file
config = load_config()

# Extract essential settings
DEBUG_MODE = config.get("debug", False)  # <--- NEW

WEBHOOK_SECRET = config.get("github_webhook_secret", "")
REPO_DEPLOY_MAP = config.get("repo_deploy_map", {})

DOCKER_COMPOSE_OPTIONS = config.get("docker_compose_options", "up -d --build")
DOCKER_COMPOSE_PATH = config.get("docker_compose_path", "docker-compose")
GIT_BRANCH = config.get("git_branch", "main")

DEPLOY_API_KEY = config.get("deploy_api_key", "")
TESTS_API_KEY = config.get("tests_api_key", "")

NOTIFICATIONS = config.get("notifications", {})
SLACK_WEBHOOK = NOTIFICATIONS.get("slack_webhook_url", "")
EMAIL_SETTINGS = NOTIFICATIONS.get("email", {})

EMAIL_SETTINGS['password'] = os.getenv("EMAIL_PASSWORD", EMAIL_SETTINGS.get('password'))
EMAIL_SETTINGS['username'] = os.getenv("EMAIL_USERNAME", EMAIL_SETTINGS.get('username'))
EMAIL_SETTINGS['smtp_server'] = os.getenv("SMTP_SERVER", EMAIL_SETTINGS.get('smtp_server'))
EMAIL_SETTINGS['smtp_port'] = int(os.getenv("SMTP_PORT", EMAIL_SETTINGS.get('smtp_port', 587)))
EMAIL_SETTINGS['use_tls'] = os.getenv("EMAIL_USE_TLS", str(EMAIL_SETTINGS.get('use_tls', True))).lower() == "true"

if not EMAIL_SETTINGS.get('username') or not EMAIL_SETTINGS.get('password'):
    logger.warning("Email username or password is missing. Email notifications may fail.")
if not EMAIL_SETTINGS.get('recipients'):
    logger.warning("No email recipients configured. Email notifications will not be sent.")

logger.info(f"Git branch: {GIT_BRANCH}")
logger.info(f"Docker compose path: {DOCKER_COMPOSE_PATH}")
logger.info(f"Email SMTP Server: {EMAIL_SETTINGS.get('smtp_server')}")
logger.info(f"Email Recipients: {EMAIL_SETTINGS.get('recipients')}")
