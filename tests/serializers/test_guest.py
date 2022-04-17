from unittest.mock import MagicMock

from marshmallow.exceptions import ValidationError

from kokon.serializers import GuestSchema


def test_claimed_at_dump_only():
    try:
        GuestSchema().load(
            {
                "guid": "5e42beb8-00a8-4577-8d2b-8ae29257a111",
                "fullName": "Marta Andrzejak",
                "email": "auz-oxloij-dxfv@yahoo.com",
                "phoneNumber": "499-330-497",
                "peopleInGroup": 4,
                "adultMaleCount": 0,
                "adultFemaleCount": 2,
                "childrenAges": [1, 10],
                "havePets": False,
                "howLongToStay": "1w",
                "claimedAt": "2022-01-01",
            },
            session=MagicMock(),
        )
    except ValidationError as e:
        assert e.messages == {"claimedAt": ["Unknown field."]}
    else:
        raise AssertionError("Exception not raised!")


def test_accommodation_unit_id():
    payload = {
        "childrenAges": [4, 10],
        "desiredDestination": "",
        "documentNumber": "vjktty",
        "email": "hkqparb@o2.pl",
        "financeStatus": "cghkgi",
        "foodAllergies": "",
        "fullName": "Monika Barbara Jasińska",
        "glutenFreeDiet": False,
        "howLongToStay": "3 w",
        "isAgent": False,
        "lactoseFreeDiet": False,
        "meatFreeDiet": False,
        "peopleInGroup": 15,
        "adultFemaleCount": 5,
        "adultMaleCount": 0,
        "petsDescription": "cfukr7iby8o",
        "havePets": False,
        "phoneNumber": "543854896",
        "priorityDate": "2022-03-20",
        "priorityStatus": "ACCOMMODATION_FOUND",
        "specialNeeds": "",
        "verificationStatus": "CREATED",
        "accommodationUnitId": None,
    }

    try:
        GuestSchema().load(payload, session=MagicMock())
    except ValidationError:
        pass
    else:
        raise AssertionError("Exception not raised.")


def test_load():
    payload = {
        "childrenAges": [4, 10],
        "desiredDestination": "",
        "documentNumber": "vjktty",
        "email": "hkqparb@o2.pl",
        "financeStatus": "cghkgi",
        "foodAllergies": "",
        "fullName": "Monika Barbara Jasińska",
        "glutenFreeDiet": False,
        "howLongToStay": "3 w",
        "isAgent": False,
        "lactoseFreeDiet": False,
        "meatFreeDiet": False,
        "peopleInGroup": 15,
        "adultFemaleCount": 5,
        "adultMaleCount": 0,
        "petsDescription": "cfukr7iby8o",
        "havePets": False,
        "phoneNumber": "543854896",
        "priorityDate": "2022-03-20",
        "priorityStatus": "ACCOMMODATION_FOUND",
        "specialNeeds": "",
        "verificationStatus": "CREATED",
        "accommodationUnitId": "008c0243-0060-4d11-9775-0258ddac7620",
    }

    GuestSchema().load(payload, session=MagicMock())
