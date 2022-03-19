accommodation_front_to_db = {
    "hostId": "host_id",
    "city": "city",
    "zip": "zip",
    "voivodeship": "voivodeship",
    "addressLine": "address_line",
    "vacanciesTotal": "vacancies_total",
    "petsPresent": "have_pets",
    "petsAccepted": "accepts_pets",
    "disabledPeopleFriendly": "disabled_people_friendly",
    "lgbtFriendly": "lgbt_friendly",
    "parkingPlaceAvailable": "parking_place_available",
    "easyAmbulanceAccess": "easy_ambulance_access",
    "ownerComments": "owner_comments",
    "staffComments": "staff_comments",
    "vacanciesFree": "vacancies_free",
    "status": "status",
}


def map_accommodation_from_front_to_db(input):
    return dict((accommodation_front_to_db[name], val) for name, val in input.items())


host_front_to_db = {
    "fullName": "full_name",
    "email": "email",
    "phoneNumber": "phone_number",
    "callAfter": "call_after",
    "callBefore": "call_before",
    "comments": "comments",
    "status": "status",
    "languagesSpoken": "languages_spoken",
}


def map_host_from_front_to_db(input):
    return dict((host_front_to_db[name], val) for name, val in input.items())
