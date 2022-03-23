from unittest.mock import MagicMock

from marshmallow.exceptions import ValidationError

from utils.serializers import GuestSchema


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
