# cipher_task
An fastapi app with BasicAuth, encoding and decoding string.
- version python 3.9
- version fastapi 0.7

## Docker build
```
$ docker build -t fastapi .
$ docker run -p 8000:8000 fastapi
```

# How to use
```
$ uvicorn main:app --reload
```

# Unit tests
from project root: github/task
```
$ pytest tests.py
```
