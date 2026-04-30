# TTS Avatar: Iván Cepeda Castro 🇨🇴

Este proyecto tiene como objetivo la creación de un **avatar digital interactivo** del senador colombiano **Iván Cepeda Castro**. El propósito principal es servir como una herramienta de **entrenamiento de comunicación**, permitiendo simular interacciones, debates y entrevistas con el perfil del candidato/político para preparar a equipos de trabajo o evaluar estrategias discursivas.

## 🎯 Idea del Proyecto

La idea central es capturar no solo la voz (TTS - Text to Speech), sino también el **estilo argumentativo, el léxico y la postura política** de Iván Cepeda. Para lograr esto, el proyecto construye un corpus robusto a partir de sus intervenciones públicas, discursos en plaza pública y análisis judiciales (especialmente sobre el proceso contra Álvaro Uribe).

### Casos de Uso:
*   **Simulación de Debates**: Entrenamiento para responder a los argumentos y el estilo pausado pero contundente del senador.
*   **Análisis de Discurso**: Estudio sistemático de las entidades, lugares y temas recurrentes en su narrativa política.
*   **Preservación Digital**: Creación de una base de conocimiento estructurada sobre su trayectoria y posiciones.

## 🛠️ Componentes y Pipeline

El proyecto utiliza un flujo de procesamiento de datos avanzado para transformar subtítulos automáticos de baja calidad en un dataset de alta fidelidad:

1.  **Extracción (Notebooks)**: Descarga de subtítulos auto-generados de YouTube.
2.  **Corrección ASR (LLM)**: Uso de modelos de lenguaje (GPT/Gemini) con un [System Prompt especializado](system_prompt_corrector.md) que corrige errores fonéticos típicos del español colombiano y nombres propios del conflicto armado (ej. "Monzáve" -> "Monsalve").
3.  **Estructuración**: Generación de archivos JSON que incluyen:
    *   Texto corregido.
    *   Resumen de la intervención.
    *   Entidades mencionadas (personas, lugares, organizaciones).
4.  **Perfilado**: Definición detallada de la personalidad y biografía del senador en [perfil.md](perfil.md).

## 📂 Estructura del Repositorio

*   `corpus_youtube.csv`: Base de datos cruda con los enlaces y metadatos de los videos.
*   `procesador_con_metadatos.py`: Script principal que automatiza el envío de fragmentos al LLM para su limpieza y análisis.
*   `correcciones_json/`: Carpeta que contiene los resultados procesados listos para entrenamiento.
*   `perfil.md`: Documento de referencia con la biografía, logros y causas del senador.
*   `system_prompt_corrector.md`: La "inteligencia" detrás de la limpieza de datos, con reglas específicas para el contexto colombiano.
*   `calcular_metricas.py`: Herramienta para evaluar el tamaño y la calidad del corpus recolectado.

## 🚀 Cómo empezar

1.  **Preparar el entorno**:
    ```bash
    conda activate pitchlab
    ```
2.  **Procesar datos**:
    Ejecuta el procesador para limpiar los subtítulos y generar el dataset estructurado:
    ```bash
    python procesador_con_metadatos.py
    ```
3.  **Verificar métricas**:
    ```bash
    python calcular_metricas.py
    ```

## ⚖️ Ética y Transparencia

Este avatar es una herramienta de **entrenamiento y análisis**. Su uso debe respetar la integridad del personaje público y no debe ser utilizado para la creación de *deepfakes* malintencionados o desinformación.

---
*Proyecto desarrollado para el entrenamiento de comunicación política y análisis de discurso.*
