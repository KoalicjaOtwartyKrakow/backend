from abc import ABC
from dataclasses import dataclass
import dateutil.parser
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

from .orm import Base, Host, AccommodationUnit, Guest


class ParseError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors

    def __str__(self):
        return f"Parse error: {','.join(self.errors)}"

    def __repr__(self):
        return f"Parse error: {','.join(self.errors)}"


@dataclass
class ParserResult:
    success: bool
    payload: Optional[Type[Base]] = None
    warnings: Optional[List[str]] = None
    errors: Optional[List[str]] = None


class Parser(ABC):
    required_fields: Dict[str, Type]
    optional_fields: Dict[str, Type]

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> Type[Base]:
        pass

    @classmethod
    def all_fields(cls):
        return {**cls.required_fields, **cls.optional_fields}


def parse_datetime(dt: Any) -> Union[str, datetime]:
    if not dt:
        return None
    try:
        return dateutil.parser.parse(dt)
    except dateutil.parser.ParserError as e:
        return str(e)


class HostParser(Parser):
    required_fields: Dict[str, Type] = {
        "fullName": str,
        "email": str,
        "phoneNumber": str,
    }
    optional_fields: Dict[str, Type] = {
        "callAfter": str,
        "callBefore": str,
        "comments": str,
        "languagesSpoken": list,
    }

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> Host:
        errors = []

        full_name = data["fullName"]
        email = data["email"]
        phone_number = data["phoneNumber"]
        call_after = data.get("callAfter")
        call_before = data.get("callBefore")
        comments = data.get("comments")

        # TODO: ask about how we deal with languages
        languages_spoken = list(
            filter(
                lambda x: x,
                map(
                    lambda l: l["code2"] if l else None, data.get("languagesSpoken", [])
                ),
            )
        )

        if errors:
            raise ParseError(errors)

        return Host(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            call_after=call_after,
            call_before=call_before,
            comments=comments,
            languages_spoken=languages_spoken,
        )


class AccommodationParser(Parser):
    required_fields: Dict[str, Type] = {
        "hostId": str,
        "city": str,
        "zip": str,
        "voivodeship": str,
        "addressLine": str,
        "vacanciesTotal": int,
    }
    optional_fields: Dict[str, Type] = {
        "petsPresent": bool,
        "petsAccepted": bool,
        "disabledPeopleFriendly": bool,
        "lgbtFriendly": bool,
        "parkingPlaceAvailable": bool,
        "easyAmbulanceAccess": bool,
        "ownerComments": str,
        "staffComments": str,
        "vacanciesFree": int,
        "status": str,
    }

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> AccommodationUnit:
        # parse required arguments
        host_id = data["hostId"]
        city = data["city"]
        zip = data["zip"]
        voivodeship = data["voivodeship"]
        address_line = data["addressLine"]
        vacancies_total = data["vacanciesTotal"]

        # parse optional arguments
        have_pets = data.get("petsPresent")
        accepts_pets = data.get("petsAccepted")
        disabled_people_friendly = data.get("disabledPeopleFriendly")
        lgbt_friendly = data.get("lgbtFriendly")
        parking_place_available = data.get("parkingPlaceAvailable")
        easy_ambulance_access = data.get("easyAmbulanceAccess")
        owner_comments = data.get("ownerComments")
        staff_comments = data.get("staffComments")
        vacancies_free = data.get("vacanciesFree")
        status = data.get("status")

        return AccommodationUnit(
            host_id=host_id,
            city=city,
            zip=zip,
            voivodeship=voivodeship,
            address_line=address_line,
            vacancies_total=vacancies_total,
            have_pets=have_pets,
            accepts_pets=accepts_pets,
            disabled_people_friendly=disabled_people_friendly,
            lgbt_friendly=lgbt_friendly,
            parking_place_available=parking_place_available,
            easy_ambulance_access=easy_ambulance_access,
            owner_comments=owner_comments,
            staff_comments=staff_comments,
            vacancies_free=vacancies_free,
            status=status,
        )


class GuestParserCreate(Parser):
    required_fields: Dict[str, Type] = {
        "fullName": str,
        "email": str,
        "phoneNumber": str,
    }
    optional_fields: Dict[str, Type] = {
        "peopleInGroup": int,
        "adultMaleCount": int,
        "adultFemaleCount": int,
        "childrenAges": list,
        "havePets": bool,
        "petsDescription": str,
        "specialNeeds": str,
        # "foodAllergies": str, # TODO: not in db
        # "meatFreeDiet": bool, # TODO: not in db
        # "glutenFreeDiet": bool, # TODO: not in db
        # "lactoseFreeDiet": bool, # TODO: not in db
        "financeStatus": str,
        "howLongToStay": str,
        "desiredDestination": str,
        "priorityStatus": str,
        "priorityDate": str,
    }

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> Guest:
        # parse required arguments
        full_name = data["fullName"]
        email = data["email"]
        phone_number = data["phoneNumber"]

        # parse optional arguments
        # is_agent = data.get("*****") # TODO: is_agent is missing in API?
        # document_number = data.get("*****") # TODO: document_number is missing in API?
        people_in_group = data.get("peopleInGroup")
        adult_male_count = data.get("adultMaleCount")
        adult_female_count = data.get("adultFemaleCount")
        # children_count = data.get("*****") # TODO: children_count is missing in API?
        children_ages = data.get("childrenAges")
        have_pets = data.get("havePets")
        pets_description = data.get("petsDescription")
        special_needs = data.get("specialNeeds")
        priority_date = data.get("priorityDate")
        # status = data.get("*****") # TODO: what is this?
        priority_status = data.get("priorityStatus")
        finance_status = data.get("financeStatus")
        how_long_to_stay = data.get("howLongToStay")
        # volunteer_note = data.get("******") # TODO: volunteer_note is missing in API?
        # validation_notes = data.get("******") # TODO: volunteer_note missing in API?
        # created_at = data.get("******") # Should not be settable for user
        # updated_at = data.get("******") # Should not be settable for user
        # id = data.get("******") # Should not be settable for user
        # guid = data.get("******") # Should not be settable for user

        return Guest(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            people_in_group=people_in_group,
            adult_male_count=adult_male_count,
            adult_female_count=adult_female_count,
            # children_count=children_count, # TODO: children_count is missing in API?
            children_ages=children_ages,
            have_pets=have_pets,
            pets_description=pets_description,
            special_needs=special_needs,
            priority_date=priority_date,
            # status=status, # TODO: what is this?
            priority_status=priority_status,
            finance_status=finance_status,
            how_long_to_stay=how_long_to_stay,
            # volunteer_note=volunteer_note, # TODO: volunteer_note is missing in API?
            # created_at=created_at,
            # updated_at=updated_at,
        )


def parse(data: Dict[str, Any], cls: Type[Parser]) -> ParserResult:
    if type(data) is not dict:
        return ParserResult(errors=["Malformed data"], success=False)

    missing_fields = [rf for rf in cls.required_fields if rf not in data.keys()]
    if missing_fields:
        return ParserResult(
            errors=[f"Missing field {f}" for f in missing_fields], success=False
        )

    wrong_types = [
        (f, t)
        for f, t in cls.all_fields().items()
        if f in data and type(data[f]) is not t
    ]
    if wrong_types:
        return ParserResult(
            errors=[
                f"Wrong field type for {f}; got {type(data[f])}, expected {t}"
                for f, t in wrong_types
            ],
            success=False,
        )

    warnings = [
        f"Additional field: {k}"
        for k in data.keys()
        if k not in cls.required_fields and k not in cls.optional_fields
    ]

    try:
        payload = cls.parse(data)
        return ParserResult(success=True, payload=payload, warnings=warnings)

    except ParseError as e:
        return ParserResult(errors=e.errors, success=False)
