# Backend for KOK

## Before you start

Dev environment:
1. make a virtual environment (Python 3.9,  use [pyenv](https://github.com/pyenv/pyenv))
2. `pip install pipenv`
3. `pipenv install --dev` (passing `--dev` will include both the default and development)
4. `pre-commit install`
5. `docker-compose up --no-start && docker-compose start` (install [Docker Desktop](https://www.docker.com/products/docker-desktop/))
6. `export IS_LOCAL_DB=True`
7. `db_user=postgres db_pass=postgres db_app_user=app db_app_pass=secret alembic upgrade head`
8. `python main.py seed --teryt-path=<path to teryt> --count=5 --db` (see `kokon/commands/seed/README.md`)

Regarding branching:
- try to make sure you work on issues on seperate branches (e.g. feature/get-guests)
- always merge to dev
- merge to main only from dev

[Pipenv](https://pipenv-fork.readthedocs.io):
- we use it as requirements.txt alternative
- we still need `requirements.txt` for cloud functions
- to generate `requirements.txt`: `pipenv lock -r > requirements.txt`

Migrations using [alembic](https://alembic.sqlalchemy.org/en/latest/):
- upgrade: `db_user=postgres db_pass=postgres db_app_user=app db_app_pass=secret alembic upgrade head`
- downgrade: `db_user=postgres db_pass=postgres db_app_user=app db_app_pass=secret alembic downgrade -1`
- new migration: `db_user=postgres db_pass=postgres db_app_user=app db_app_pass=secret alembic revision --autogenerate -m <migration_name>` (then edit generated migration if required)
- after migration added - ensure in dev that downgrade works properly

## Testing

```bash
IS_LOCAL_DB=True db_user=postgres db_pass=postgres db_app_user=app_test db_app_pass=secret db_name=kokon_test alembic upgrade head

pytest tests
```

If you need database filled with data - use `db` fixture, just add `db` argument to your test function.

### Coverage report

You can take a look at a coverage report in `htmlcov/index.html` file inside root directory.

## Debugging

You can run Google Cloud Function by running:
```
$ export IS_LOCAL_DB=True
$ functions-framework --target <function-name> --debug
```

Arguments (including request payload) should be passed as query params.

You'll need to add a header with the following value as well. Either pass it with `-H` to curl,
or install a browser extension that allows customizing headers. For example header hacker for Chrome.

```
X-Endpoint-API-UserInfo: eyJnaXZlbl9uYW1lIjogIkpvaG4iLCAiZmFtaWx5X25hbWUiOiAiRG9lIiwgImVtYWlsIjogImpvaG4uZG9lQGV4YW1wbGUuY29tIiwgInN1YiI6ICIxMDc2OTE1MDM1MDAwNjE1MDcxNTExMzA4MjM2NyIsICJwaWN0dXJlIjogImh0dHBzOi8vZ29vZ2xlLmNvbS8xMjMifQ==
```

For more info see: https://cloud.google.com/endpoints/docs/openapi/migrate-to-esp-v2#receiving_auth_results_in_your_api

You can debug functions using tests, see `tests/functions` for examples.

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
