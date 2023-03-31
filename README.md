# Cellular Automata Simulation App

This project is visualisation tool for cellular automata, focused primarily around Conway's Game of Life, however, dditional rules for celluar automata are available to experiment with.

This project is developed by:
**Sean Nelson** *(ll17s2n)* and **Steven Taylor** *(sc18sst)*

## Setup

This project is managed with [poetry](https://python-poetry.org/), which can be installed on Linux/Mac/WSL by:
```shell
curl -sSL https://install.python-poetry.org | python3 -
```

The application's packages can then be installed by running:
```shell
poetry install
```
inside of the base directory

## Usage

The application can then be run by:
```shell
poetry run python3 main.py
```

## Testing

You can run the tests for this application by:
```shell
poetry run pytest
```