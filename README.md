# Backend for KOK

1. [Before you start](#before-you-start)
2. [API Documentation](#api-documentation)
    1. [Accommodation](#accommodation)
    2. [Host](#host)
    3. [Guest](#guest)
    4. [Teammember](#teammember)

## Before you start

0. Make sure you are developing on dev branch!
1. Make a virtual environment.
2. `pip install -r requirements.txt`
3. `pre-commit install`

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

## API Documentation

### Accommodation

`POST /accommodation`

Parameters:
| Parameter       | Description                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------|
| city            | city in which apartment is located                                                              |
| zip             | **(required)** zip code of apartment                                                            |
| voivodeship     | voivodeship of apartment.                                                                       |
| address_line    | **(required)** address of apartment                                                             |
| vacancies_total | **(required)** total vacancies of apartment                                                     |
| vacancies_free  | **(required)** vacancies left for apartment                                                     |
| have_pets       | True if apartment owner has pets, False otherwise                                               |
| accept_pets     | True if apartment owner accepts pets, False otherwise                                           |
| comments        | additional comments on apartment                                                                |
| status          | apartment verification status. Must be one of: 'added', 'phone_verified', 'in_person_verified'. |

Sample request:
```json
{
    "city": "Kraków",
    "zip": "30-337",
    "voivodeship": "Lesser Poland",
    "address_line": "ul. Żadna 3/4",
    "vacancies_total": 9,
    "vacancies_free": 9,
    "have_pets": True,
    "accept_pets": True,
    "comments": "I love animals!",
    "status": "in_person_verified"
}
```

Possible responses:
- 200: apartment successfully added
- 400: invalid request parameters or db transaction error

`GET /accommodation/:accommodationId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /accommodation/:accommodationId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /accommodation/:accommodationId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`GET /accommodation/findByNeeds`

Parameters:

Sample request:
```

```

Sample response:
```

```

---

### Host

`POST /host`

Parameters:

Sample request:
```

```

Sample response:
```

```

`GET /hosts/:hostId`

Parameters:

Sample request:
```

```

Sample response:
```

```


`POST /host/:hostId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /host/:hostId`

Parameters:

Sample request:
```

```

Sample response:
```

```

---
### Guest

`POST /guest`

Parameters:

Sample request:
```

```

Sample response:
```

```

`GET /guest/:guestId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /guest/:guestId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /guest/:guestId`

Parameters:

Sample request:
```

```

Sample response:
```

```

### Teammember

`POST /teammember`

Parameters:

Sample request:
```

```

Sample response:
```

```

`GET /teammember/:teammemberId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /teammember/:teammemberId`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /teammember/:teammember`

Parameters:

Sample request:
```

```

Sample response:
```

```