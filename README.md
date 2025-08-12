# FastAPI PDF Analyzer

A simple FastAPI app to analyze PDF files and extract structured data using an LLM (OpenAI-compatible API or local models with ollama).

## Setup

1. **Clone the repository**

2. **Install [uv](https://github.com/astral-sh/uv) (if not already installed):**
   ```sh
   pip install uv
   ```

3. **Install dependencies:**
   ```sh
   uv sync
   ```

4. **Set up environment variables:**
   ```sh
   cp .env.example .env
   ```
   and set your API key if needed.

5. **Start the FastAPI server:**
   ```sh
   uv run main.py
   ```
   The API will be available at http://localhost:8000

6. **Test the API:**
   - Make sure the server is running.
   - Run the test script:
     ```sh
     uv run tests/test_api.py
     ```

## Endpoints

- `POST /analyze-pdf` — Upload a PDF and get extracted data.

## Notes
- Requires Python 3.9+
- For local LLM (Ollama), make sure Ollama is running and accessible at the configured base URL.

## Switching between local (Ollama) and OpenAI models

Use the LOCAL_MODE flag in your .env to switch providers:

- Local (Ollama):
   - Ensure Ollama is running
   - LOCAL_MODE=True
   - MODEL_NAME=llama2 (or any Ollama-installed model)

- OpenAI or other hosted model:
   - LOCAL_MODE=False
   - OPENAI_API_KEY=... (your OpenAI API key)
   - MODEL_NAME=gpt-4o-mini (or another available OpenAI model)

After updating .env, restart the server.
