from gpt4all import GPT4All
import torch
import warnings
import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
)

logger = logging.getLogger(__name__)
__gpt_model = None

def load_model():
    global __gpt_model

    if __gpt_model is None:
        logger.info("Cargando modelo por primera vez...")
        # Obtener la lista de modelos disponibles
        available_models = GPT4All.list_models()

        # Buscar el modelo "Llama 3 8B Instruct" en la lista
        model_name = None
        for model in available_models:
            if "Llama 3 8B Instruct" in model["name"]:  # Busca por nombre parcial
                model_name = model["filename"]
                break

        if not model_name:
            raise Exception("❌ No se encontró el modelo de LLaMA 3 8B en la lista de modelos disponibles.")

        logger.info(f"📥 Modelo encontrado: {model_name}")

        # Cargar el modelo
        if torch.cuda.is_available():
            print(f"✅ Ejecutando en GPU: {torch.cuda.get_device_name(0)}")
            __gpt_model = GPT4All(model_name, device="gpu")
        else:
            warnings.warn("⚠ No se detectó GPU. Ejecutando en CPU, puede ser más lento.")
            __gpt_model = GPT4All(model_name)

        logger.info("✅ Modelo cargado correctamente.")

def ask(message: str, from_number: str) -> str:
    # Asegurar que el modelo esté cargado
    load_model()

    # Generar respuesta
    response = __gpt_model.generate(
        prompt=message,
        max_tokens=250,
        temp=0.7,
        top_k=40,
        top_p=0.9,
        repeat_penalty=1.15,
    )

    return response
