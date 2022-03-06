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
| Parameter       | Description                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------|
| id              | **(required)** id of the apartment to show                                                          |
| city            | city in which apartment is located                                                              |
| zip             | **(required)** zip code of apartment                                                                |
| voivodeship     | voivodeship of apartment. Must be one of:                                                       |
| address_line    | **(required)** address of apartment                                                                 |
| vacancies_total | **(required)** total vacancies of apartment                                                         |
| vacancies_free  | **(required)** vacancies left for apartment                                                         |
| have_pets       | True if apartment owner has pets, False otherwise                                               |
| accept_pets     | True if apartment owner accepts pets, False otherwise                                           |
| comments        | additional comments on apartment                                                                |
| status          | apartment verification status. Must be one of: 'added', 'phone_verified', 'in_person_verified'. |

Sample request:
```

```

Sample response:
```

```

`POST /apartments`


`PUT /apartments`


`DELETE /apartments/:id`


---

### Hosts

`GET /hosts/:id`


`POST /hosts`


`PUT /hosts`


`DELETE /hosts/:id`

---
### Guests

`GET /guests/:id`


`POST /guests`


`PUT /guests`


`DELETE /guests/:id`