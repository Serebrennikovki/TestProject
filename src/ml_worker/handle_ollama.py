import requests
import json
from config import get_settings
from ollama_stream_error import OllamaStreamError

HOST_MODEL = 'ollama'
MODEL_NAME = 'llama3'

settings = get_settings()

def ollama_stream_to_string(prompt: str, model: str = settings.MODEL_NAME) -> str:
    url =f'http://{settings.MODEL_HOST}:11434/api/generate'

    try:
        response = requests.post(
            url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            stream=True,
            timeout=60
        )

        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise OllamaStreamError(f"ошибка обращения к Ollama {e}")
    
    result=""

    try:
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                raise OllamaStreamError(f'Некорректный json в стриме')
            
            if "error" in data:
                raise OllamaStreamError(f'Ollama error: {data['error']}')
            result += data.get("response", "")

            if data.get("done"):
                break
    except requests.exceptions.ChunkedEncodingError:
        raise OllamaStreamError('Ошибка стриминга(обрыв соединения)')
    except Exception as e:
        raise OllamaStreamError(f'Ошибка обработки стрима: {e}')
    
    return result
