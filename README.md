# Backend for KOK

## Before you start

Dev environment:
1. make a virtual environment (Python 3.9,  use [pyenv](https://github.com/pyenv/pyenv))
2. `pip install pipenv`
3. `pipenv install --dev` (passing `--dev` will include both the default and development)
4. `pre-commit install`
5. `docker-compose up --no-start && docker-compose start` (install [Docker Desktop](https://www.docker.com/products/docker-desktop/))
6. `export IS_LOCAL_DB=True`
7. `alembic upgrade head`
8. `PYTHONPATH=. python utils/data-generator/main.py --teryt-path=<path to teryt> --count=5 --db`

Regarding branching:
- try to make sure you work on issues on seperate branches (e.g. feature/get-guests)
- always merge to dev
- merge to main only from dev

[Pipenv](https://pipenv-fork.readthedocs.io):
- we use it as requirements.txt alternative
- we still need `requirements.txt` for cloud functions
- to generate `requirements.txt`: `pipenv lock -r > requirements.txt`

Migrations using [alembic](https://alembic.sqlalchemy.org/en/latest/):
- upgrade: `alembic upgrade head`
- downgrade: `alembic downgrade -1`
- new migration: `alembic revision --autogenerate -m <migration_name>` (then edit generated migration if required)
- after migration added - ensure in dev that downgrade works properly

## Testing

```bash
IS_LOCAL_DB=True db_name=kokon_test alembic upgrade head

pytest tests
```

If you need database filled with data - use `db` fixture, just add `db` argument to your test function.

## Debugging

You can run Google Cloud Function by running:
```
$ export IS_LOCAL_DB=True
$ functions-framework --target <function-name> --debug
```

Arguments (including request payload) should be passed as query params.

You'll need to add an authorization header with the following value as well. Either pass it with `-H` to curl,
or install a browser extension that allows customizing headers. For example header hacker for Chrome.

```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJnaXZlbl9uYW1lIjoiSm9obiIsImZhbWlseV9uYW1lIjoiRG9lIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsInN1YiI6IjEwNzY5MTUwMzUwMDA2MTUwNzE1MTEzMDgyMzY3IiwicGljdHVyZSI6Imh0dHBzOi8vZ29vZ2xlLmNvbS8xMjMifQ.kVDaaGkjVeRgbM0AbQhQQy9LlgpdCpbgq32-BuFLjObQZ4FEiYEZdKKh_u3BZVKiYftGtvFCRmNQ07KTugZXBz7RrXH-qM_UilN7A6i-rxPTAVW56AP7Hh8zOyCAn7lTrnTdkH1ujGx7zNo2sE9k9J5OzObtsc6TLbPS5q5_07SBVL1dll2hP84-kslMfi5ThxN61nv5ImKpY2C5zqQJvKMMfHo1o9UIYXSb99sYN6uy_uERGdJQP3IhOnQjSX6ldnCwMHzXwgGQztDfLuGWXoYc2UY9s6XkLX5d5_ndMrP5z1n7uZu7I7of75bSEgaEt4QLl-asGqCykQiPBaQ0AQ
```

This value is an (purposefully) invalid jwt, but because the validation of JWTs (at least now) happens before requests
hit the backend, our backend accepts any JWTs, without checking the signature.

### Generating SQL from orm

For example for the `Host` model:
`print(CreateTable(Host.__table__).compile(global_pool))`

Passing a working postgres connection pool is important, otherwise some features (like native enums) are not used.

## Relationship with the infrastructure as code repo

* The OpenAPI spec now lives in the iac repo
  * Dev: https://github.com/KoalicjaOtwartyKrakow/iac/blob/dev/env/dev/api.yaml
  * Prod: https://github.com/KoalicjaOtwartyKrakow/iac/blob/dev/env/prod/api.yaml
* When adding/removing functions add/remove them from the cloudbuild setup as well at:
  https://github.com/KoalicjaOtwartyKrakow/iac/blob/dev/modules/codebuild/backend/main.tf#L6
