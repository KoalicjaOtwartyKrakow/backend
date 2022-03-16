#!/bin/bash

pkill -f 'bin/functions-framework --target'

export PROJECT_ID=blah
export IS_LOCAL_DB=True
export db_user=postgres
export db_pass=postgres
export db_name=salamlab-apartments
functions-framework --target get_all_guests --debug --port 6201&
functions-framework --target add_guest --debug --port 6202&
functions-framework --target get_guest_by_id --debug  --port 6203&
functions-framework --target delete_guest --debug  --port 6204&
functions-framework --target update_guest --debug  --port 6205&

#####################################
### Test Queries
#####################################

# curl 'http://172.19.93.35:6201/guest/' -X GET

# curl 'http://172.19.93.35:6202/guest/' -X POST -H 'Content-Type: application/json' --data-raw $'{\n   "adult_female_count":1,\n   "adult_male_count":1,\n   "children_ages":[\n  10,\n      11\n   ],\n   "children_count":2,\n   "email":"jon.doe@google.com",\n   "full_name":"Jon Doe",\n   "people_in_group":4,\n   "phone_number":"123-456-789"\n}'

# curl 'http://172.19.93.35:6203/guest/2c48d183-c9a0-419b-92d5-a7ff6806b480' -X GET

# curl 'http://172.19.93.35:6204/guest/2c48d183-c9a0-419b-92d5-a7ff6806b480' -X DELETE

# curl 'http://172.19.93.35:6205/guest/962efb32-cb96-4872-b1dd-6338fcb3af9f' -X POST -H 'Content-Type: application/json' --data-raw $'{\n   "adult_female_count":3,\n   "adult_male_count":0,\n   "children_ages":[\n      10,\n      11\n   ],\n   "children_count":2,\n   "people_in_group":5\n}'
