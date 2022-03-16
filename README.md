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
| Parameter          | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| full_name          | **(required)**                                                             
| email              | **(required)**                                                            
| phone_number       |                                                                      
| people_in_group    | **(required)**                                                  
| adult_male_count   | **(required)**                                                
| adult_female_count | **(required)**                                              
| children_count     | **(required)**                                          
| children_ages      |                                                   
| have_pets          |  
| pets_description   |  
| special_needs      |  
| finance_status     | 
| how_long_to_stay   |  
| volunteer_note     |


Sample request:
```json
{
    "full_name": "Jan Kowalski",
    "email" : "jan@kowalski.pl",
    "phone_number": "654-654-654",
    "people_in_group": 5,
    "adult_male_count":1,
    "adult_female_count":2,
    "children_count":2,
    "children_ages":[1,5],
    "have_pets":true,
    "pets_description":"1 small dog",
    "special_needs" : "No special needs",
    "finance_status" : "Some finance status.",
    "how_long_to_stay" : 1,
    "volunteer_note" : "Some note."
}
```

Possible responses:
- 201: guest successfully created
- 405: invalid input

`GET /guest/:guestId`

Parameters:

'guestId'

Sample request:
```
`GET /get_guest_by_id?guestId=21`
```

Sample response:
```json
{
    "adult_female_count": 2,
    "adult_male_count": 1,
    "children_ages": [
        1,
        5
    ],
    "children_count": 2,
    "created_at": "2022-03-11 17:08:59.170341",
    "email": "jan@kowalski.pl",
    "finance_status": "Some finance status.",
    "full_name": "Jan Kowalski",
    "guid": "8d0bb783-7165-41c5-ada7-a0274f48c991",
    "have_pets": true,
    "how_long_to_stay": "1",
    "id": 2,
    "people_in_group": 5,
    "pets_description": "1 small dog",
    "phone_number": "654-654-654",
    "priority_date": "2022-03-11 17:08:59.170341",
    "special_needs": "No special needs",
    "status": "CREATED",
    "updated_at": null,
    "volunteer_note": null
}

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