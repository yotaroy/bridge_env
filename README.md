# Contract Bridge Environment for Python

bridge_env is a python package for contract bridge.
bridge_env supports a network bridge used in the World Computer Bridge Championships.

## Install bridge_env

Run on the root directory of this repository.

```bash
pip install .
```

Install with packages for development, run

```bash
pip install .[dev]
```

## Network bridge

Protocol is [version 18](http://www.bluechipbridge.co.uk/protocol.htm).

Run server.

```bash
bridge-server [-h] [-p PORT] [-i IP_ADDRESS]

# optional arguments:
#   -h, --help            show this help message and exit
#   -p PORT, --port PORT  Port number. (default=2000)
#   -i IP_ADDRESS, --ip_address IP_ADDRESS
#                         IP address. (default=localhost)
```

Run an example client.

```bash
usage: bridge-client-ex [-h] [-p PORT] [-i IP_ADDRESS] [-l LOCATION] [-t TEAM_NAME]

# optional arguments:
#   -h, --help            show this help message and exit
#   -p PORT, --port PORT  Port number. (default=2000)
#   -i IP_ADDRESS, --ip_address IP_ADDRESS
#                         IP address. (default=localhost)
#   -l LOCATION, --location LOCATION
#                         Player (N, E, S or W)
#   -t TEAM_NAME, --team_name TEAM_NAME
#                         Team name
```

## Requirements

- Python >= 3.7
- numpy

## For development

### Requirements for development

- flake8
- mypy
- pytest
- pytest-mock

You can install them from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Test

```bash
pytest -vv
```

### Type check

```bash
mypy --ignore-missing-imports .
```

### Lint

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

flake8 . --count --exit-zero --max-complexity=10 --max-line-length=80 --statistics
```

## License

[MIT License](./LICENSE)
