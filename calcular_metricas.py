import pandas as pd
import re
import os

def calcular_metricas(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: No se encuentra el archivo {csv_path}")
        return

    # Cargamos el CSV con el separador detectado (;)
    # utf-8-sig maneja el BOM que suele poner Excel
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # Verificar que existe la columna 'texto'
    if 'texto' not in df.columns:
        print("Error: El CSV no tiene una columna llamada 'texto'")
        return

    # Limpiamos posibles valores nulos
    df['texto'] = df['texto'].fillna('')

    # 1. Caracteres (incluyendo espacios)
    df['n_caracteres'] = df['texto'].str.len()

    # 2. Palabras (split por espacios)
    df['n_palabras'] = df['texto'].apply(lambda x: len(x.split()))

    # 3. Tokens (Palabras + signos de puntuación como elementos separados)
    def simple_tokenizer(text):
        # Busca palabras (letras/números) o cualquier carácter que no sea espacio
        return len(re.findall(r'\w+|[^\w\s]', text, re.UNICODE))

    df['n_tokens'] = df['texto'].apply(simple_tokenizer)

    # Mostrar resultados por fila (primeras 5)
    print("\n--- Métricas por video (Primeros 5) ---")
    print(df[['video_id', 'n_palabras', 'n_tokens', 'n_caracteres']].head())

    # Totales globales
    print("\n" + "="*30)
    print("      RESUMEN TOTAL")
    print("="*30)
    print(f"Total de Videos:     {len(df)}")
    print(f"Total de Palabras:   {df['n_palabras'].sum():,}")
    print(f"Total de Tokens:     {df['n_tokens'].sum():,}")
    print(f"Total de Caracteres: {df['n_caracteres'].sum():,}")
    print("="*30)

    # Opcional: Guardar el CSV con las métricas
    # df.to_csv('corpus_con_metricas.csv', sep=';', index=False, encoding='utf-8-sig')
    # print("\nResultados guardados en 'corpus_con_metricas.csv'")

if __name__ == "__main__":
    calcular_metricas('corpus_youtube.csv')
