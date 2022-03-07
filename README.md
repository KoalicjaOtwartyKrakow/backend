# backend

Please remember to develop on *dev* branch. Better readme to follow.

## Before you start

1. Make a virtual environment.
2. `pip install -r requirements.txt`
3. `pre-commit install`

## API Documentation

### Apartments

`GET /apartments/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /apartments`

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

`PUT /apartments`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /apartments/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```

---

### Hosts

`GET /hosts/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /hosts`

Parameters:

Sample request:
```

```

Sample response:
```

```

`PUT /hosts`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /hosts/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```

---
### Guests

`GET /guests/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```

`POST /guests`

Parameters:

Sample request:
```

```

Sample response:
```

```

`PUT /guests`

Parameters:

Sample request:
```

```

Sample response:
```

```

`DELETE /guests/:id`

Parameters:

Sample request:
```

```

Sample response:
```

```