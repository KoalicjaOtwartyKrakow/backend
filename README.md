# Backend for KOK

1. [Before you start](#before-you-start)
2. [API Documentation](#api-documentation)
    1. [Accommodation](#accommodation)
    2. [Host](#host)
    3. [Guest](#guest)
    4. [Teammember](#teammember)

## Before you start

1. Make a virtual environment.
2. `pip install -r requirements.txt`
3. `pre-commit install`

Regarding branching:
- try to make sure you work on issues on seperate branches (e.g. feature/get-guests)
- always merge to dev
- merge to main only from dev

## Testing

```bash
pip install pytest
pytest tests
```

## Local debuging

To debug your Google Cloud Function locally, you need to first create database. Easiest way is to use prepared docker container:

First, install [docker](https://docs.docker.com/get-docker/)
To build container and recreate DB schema, run:
```
$ cd dockerfiles
$ ./create_debug_container.sh
```

After this you can run:
```
docker run --rm -it -p 5432:5432 test-postgres-kok
``` 
(Note: remove `--rm` if you want to keep container after shut down and use `docker start -i <container_id>` in consequetive container starts)

Than you can run Google Cloud Function by running:
```
$ export IS_LOCAL_DB=True
$ export db_user=postgres
$ export db_pass=postgres
$ export db_name=salamlab-apartments
$ functions-framework --target <function-name> --debug
```

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