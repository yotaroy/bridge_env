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
pip install '.[dev]'
```

## Network bridge

Protocol is [version 18](http://www.bluechipbridge.co.uk/protocol.htm).

Run server.

```bash
bridge-server [-h] [-p PORT] [-i IP_ADDRESS] [-b BOARD_SETTING] \
    [-r RESTART_INDEX] [-o OUTPUT_FILE]

# optional arguments:
#   -h, --help            show this help message and exit
#   -p PORT, --port PORT  Port number. (default=2000)
#   -i IP_ADDRESS, --ip_address IP_ADDRESS
#                         IP address. (default=localhost)
#   -b BOARD_SETTING, --board_setting BOARD_SETTING
#                         Board settings file (.json or .pbn).
#   -r RESTART_INDEX, --restart_index RESTART_INDEX
#                         Index of board settings to restart. (0-idx, default=0)
#   -o OUTPUT_FILE, --output_file OUTPUT_FILE
#                         Output file path (.json or .pbn file).
#                         File will be overwritten. (default="output.json")
```

If a board settings file is not set, randomly generated 100 boards setting is used.

Run an example client.

```bash
bridge-client-ex [-h] [-p PORT] [-i IP_ADDRESS] [-l LOCATION] [-t TEAM_NAME]

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

### Board setting and log formats

Server can read board settings in PBN or JSON file.
Game log outputted by server follows PBN or JSON formats below.

Board setting in JSON is defined in
[json schema](bridge_env/data_handler/json_handler/board_setting_format.schema.json).
Game log in JSON is defined in
[json schema](bridge_env/data_handler/json_handler/log_format.schema.json).
See [README](bridge_env/data_handler/json_handler/README.md) for more information
about JSON format.

Board setting in PBN (v2.1) is defined in
<http://www.tistis.nl/pbn/pbn_v21.txt> as "import format".
Game log in PBN (v2.1) is defined in
<http://www.tistis.nl/pbn/pbn_v21.txt> as "export format".
See <http://www.tistis.nl/pbn/> for more information about PBN format.

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
