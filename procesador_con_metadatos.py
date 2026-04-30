import os
import json
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import time
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN ---
# Asegúrate de que tu clave de API esté configurada como variable de entorno o búscala aquí
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "TU_API_KEY_AQUI")
INPUT_CSV = "corpus_youtube.csv"
OUTPUT_DIR = "correcciones_json"
MODEL = "gpt-4o-mini"
PROMPT_FILE = "system_prompt_corrector.md"

# Precios GPT-4o-mini (Abril 2024)
COST_INPUT_1M = 0.15
COST_OUTPUT_1M = 0.60

client = OpenAI()
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar el System Prompt quirúrgico
if os.path.exists(PROMPT_FILE):
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
else:
    raise FileNotFoundError(f"No se encontró el archivo de prompt: {PROMPT_FILE}")

def procesar_transcripcion(texto, metadata, max_retries=3):
    """Envía el texto y metadatos a OpenAI y devuelve el JSON procesado"""
    if not texto or len(texto.strip()) < 10:
        return None, 0
        
    prompt_usuario = f"""Metadatos del video:
- video_id: {metadata['video_id']}
- fecha: {metadata['fecha']}
- titulo: {metadata['titulo']}
- link: {metadata['link']}

Procesa la siguiente transcripción:

{texto}"""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0
            )
            
            # Calcular costo
            usage = response.usage
            costo_in = (usage.prompt_tokens / 1_000_000) * COST_INPUT_1M
            costo_out = (usage.completion_tokens / 1_000_000) * COST_OUTPUT_1M
            costo_total = costo_in + costo_out
            
            resultado_json = json.loads(response.choices[0].message.content)
            
            # Asegurar que los metadatos estén presentes y sean correctos
            if 'metadata' not in resultado_json:
                resultado_json['metadata'] = metadata
            else:
                # Priorizar metadatos del CSV para evitar alucinaciones
                resultado_json['metadata'].update(metadata)
                
            return resultado_json, costo_total
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"\nError (intento {attempt+1}): {e}. Reintentando en 2s...")
                time.sleep(2)
            else:
                print(f"\nError fatal tras {max_retries} intentos: {e}")
                return None, 0

def main():
    # Cargar datos
    print(f"Leyendo archivo: {INPUT_CSV}")
    try:
        df = pd.read_csv(INPUT_CSV, sep=';', encoding='utf-8-sig')
        df['texto'] = df['texto'].fillna('')
        print(f"Cargados {len(df)} registros para procesar.")
    except Exception as e:
        print(f"Error al cargar el CSV: {e}")
        return

    total_gasto_usd = 0.0
    procesados_nuevos = 0
    errores = 0

    # Limitar para pruebas
    # df = df.head(20) 

    for index, row in tqdm(df.iterrows(), total=len(df), desc="Procesando"):
        video_id = row['video_id']
        fecha = str(row['fecha'])
        
        file_name = f"{fecha}_{video_id}.json"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        # Metadatos para el prompt y el JSON
        metadata = {
            "video_id": video_id,
            "fecha": fecha,
            "titulo": row['titulo'],
            "link": row['fuente']
        }
        
        # IMPORTANTE: Si quieres reprocesar archivos para incluir las mejoras, 
        # puedes borrar la carpeta o comentar este bloque 'if'.
        if os.path.exists(file_path):
            # Opcional: Podrías cargar el archivo y verificar si ya tiene metadata
            # pero por ahora simplemente saltamos.
            continue
            
        resultado, costo = procesar_transcripcion(row['texto'], metadata)
        
        if resultado:
            # Guardar JSON con formato legible
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            
            total_gasto_usd += costo
            procesados_nuevos += 1
        else:
            errores += 1
        
    print(f"\n--- PROCESO COMPLETADO ---")
    print(f"Archivos nuevos procesados con éxito: {procesados_nuevos}")
    print(f"Registros con error: {errores}")
    print(f"Gasto total aproximado: {total_gasto_usd:.4f} USD")
    print(f"Resultados en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
