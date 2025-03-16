import logging
import sys

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def save_user(phone_number):
    return 1

def save_message(sender, receiver, message, message_type="text"):
    return 1
