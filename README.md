# Backend for KOK

## Before you start

1. Make a virtual environment.
2. `pipenv install --dev` (passing `--dev` will include both the default and development)
3. `pre-commit install`
4. `docker-compose up --no-start && docker-compose start` (install [Docker Desktop](https://www.docker.com/products/docker-desktop/))
5. `alembic upgrade head`
6. `PYTHONPATH=. python utils/data-generator/main.py --teryt-path=<path to teryt> --count=5 --db`

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
