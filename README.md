# Start with python

```
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```

## start tests

```
  pytest
```

## start api

```
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

___

# Start with docker
```
  docker-compose up --build
```
