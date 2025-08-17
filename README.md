# LLM Code Generator

A Python application that uses Large Language Models to generate and execute code solutions to programming problems.

## Features

- Generate Python code using LLM APIs (OpenAI GPT-5, Claude, Gemini)
- Execute generated code safely in isolated environment
- Configuration-based API key management
- Support for multiple LLM providers

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install requests
   ```
4. Configure API keys in `config.json`:
   ```json
   {
     "models": {
       "openai": {
         "api_key": "your-openai-api-key-here"
       }
     }
   }
   ```

## Usage

Generate and execute code:
```bash
python llm_code_generator.py "Create a Python program that calculates 10+5"
```

Generate code only (no execution):
```bash
python llm_code_generator.py "Create a sorting algorithm" --no-execute
```

Use different model provider:
```bash
python llm_code_generator.py "Hello world program" --model claude
```

## Files

- `llm_code_generator.py` - Main application
- `config_reader.py` - Configuration management
- `config.json` - API keys and model settings

## Security

- Never commit API keys to version control
- Generated code is executed in subprocess isolation
- Configurable execution timeouts