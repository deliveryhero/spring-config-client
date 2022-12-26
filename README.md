## Spring Config Server Client for Python

### Usage

Environment variables have to be defined in order to use

```bash
CONFIGSERVER_ADDRESS=
LABEL=
PROFILE=
APP_NAME=
CONFIGSERVER_AUTH_USERNAME=
CONFIGSERVER_AUTH_PASSWORD=
```

```python
from spring_config_client.conf.settings import Settings

settings = Settings()

# example usage
settings.DATABASE_URL
```

### Development

> This project is using bumpversion tool to track versions.
> Versioning should be done by developer when introducing changes.

### Tests
```tests
# single 
make test flags="-s -vv" t='test_settings_get_key_from_environ'

# all tests
make tests
```

```python
bumpversion --config-file .bumpversion.cfg minor
```

### How Variables are Resolved

```bash
# Literal value used as is
VAR1='value' 

# taken from local environment LOCAL_ENV value
VAR1='${LOCAL_ENV}' 

# value is taken from local environment LOCAL_ENV2
# if its not defined than default value is assigned 
VAR1='${LOCAL_ENV2:default}' 
```

### Installation

With make
```bash
make install
```

Manuel
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

