guest_front_to_db = {
    "fullName": "full_name",
    "email": "email",
    "phoneNumber": "phone_number",
    "peopleInGroup": "people_in_group",
    "adultMaleCount": "adult_male_count",
    "adultFemaleCount": "adult_female_count",
    "childrenAges": "children_ages",
    "havePets": "have_pets",
    "petsDescription": "pets_description",
    "specialNeeds": "special_needs",
    "priorityDate": "priority_date",
    "priorityStatus": "priority_status",
    "financeStatus": "finance_status",
    "howLongToStay": "how_long_to_stay",
}


def map_guest_from_front_to_db(input):
    return dict((guest_front_to_db[name], val) for name, val in input.items())
