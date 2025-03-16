from whatsapp import get_message, get_phone_number, send_text_answer
from chat.mistral import ask
from log.sender import save_message, format_conversation_history
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
)
logger = logging.getLogger(__name__)


def run(request: dict):
    logger.info("Incoming webhook message")
    message = get_message(request)
    phone_number = get_phone_number(request)
    logger.info(f"from: {phone_number}")

    if message:
        if message.get("type") == "text":
            _message_body = message['text']['body']
            conversation = format_conversation_history(message["from"], _message_body)
            respuesta_chatgpt = ask(conversation)

            send_text_answer(respuesta_chatgpt, message["from"], message["id"], phone_number)
            save_message(message["from"], "IA", _message_body, "text")
            save_message("IA", message["from"], respuesta_chatgpt, "text")
            logger.debug("Text answer sent ;)")
        else:
            logger.debug("pos na")
