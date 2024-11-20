# EMMA - Evolutionary Reactive Multi-agent System

This project implements an evolutionary algorithm to optimize AI agent prompts.

## Running the Project

To run the main script:

```
python main.py
```

## Docker

To build and run using Docker:

```
docker build -t elma .
docker run -e OPENAI_API_KEY=your_api_key_here elma
```

## Development

1.  Ensure you have Python 3.10 or later installed.
2.  Clone this repository.
3.  Run the setup script:
    ```
    ./setup_venv_mac.sh
    ```
4.  Activate the virtual environment:

    ```
    source venv/bin/activate
    ```

5.  run main.py
    ```
    ./venv/bin/python3 main.py
    ```

# Test

1. To run the tests, use the following command:
   `pytest
`
2. Install pre-commit hooks:

   ```
   pre-commit install
   ```

   Then, run the following command to start watch mode:

   ```
   ptw
   ```
