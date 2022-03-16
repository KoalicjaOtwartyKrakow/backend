from abc import ABC
from dataclasses import dataclass
import dateutil.parser
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

from .orm import Base, Language, Host, AccommodationUnit, Guest


class ParseError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors

    def __str__(self):
        return f"Parse error: {','.join(self.errors)}"

    def __repr__(self):
        return f"Parse error: {','.join(self.errors)}"


# TODO: discuss how to solve languages
languages = {
    "en": Language(name="English", code2="en", code3="eng"),
    "pl": Language(name="Polski", code2="pl", code3="pol"),
    "uk": Language(name="українська", code2="uk", code3="ukr"),
}


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
                map(lambda l: languages.get(l), data.get("languagesSpoken", [])),
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
        "addressline": str,
        "vacanciesTotal": int,
    }
    optional_fields: Dict[str, Type] = {
        "havePets": bool,
        "acceptsPets": bool,
        "comments": str,
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
        address_line = data["addressline"]
        vacancies_total = data["vacanciesTotal"]

        # parse optional arguments
        have_pets = data.get("havePets")
        accepts_pets = data.get("acceptsPets")
        comments = data.get("comments")
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
            comments=comments,
            vacancies_free=vacancies_free,
            status=status,
        )


class GuestParser(Parser):
    required_fields: Dict[str, Type] = {
        "full_name": str,
        "email": str,
        "phone_number": str,
        "people_in_group": int,
        "adult_male_count": int,
        "adult_female_count": int,
        "children_count": int,
        "children_ages": list,

    }
    optional_fields: Dict[str, Type] = {
        "have_pets": bool,
        "pets_description": str,
        "special_needs": str,
        "volunteer_note": str,
        "finance_status": str,
        "how_long_to_stay": int,
    }

    @classmethod
    def parse(cls, data: Dict[str, Any]) -> Guest:
        # parse required arguments
        full_name = data["full_name"]
        email = data["email"]
        phone_number = data["phone_number"]
        people_in_group = data["people_in_group"]
        adult_male_count = data["adult_male_count"]
        adult_female_count = data["adult_female_count"]
        children_count = data["children_count"]
        children_ages = data["children_ages"]

        # parse optional arguments
        have_pets = data.get("have_pets")
        pets_description = data.get("pets_description")
        special_needs = data.get("special_needs")        
        volunteer_note = data.get("volunteer_note")
        finance_status = data.get("finance_status")
        how_long_to_stay = data.get("how_long_to_stay")

        return Guest(
            full_name = full_name,
            email = email,
            phone_number = phone_number,
            people_in_group = people_in_group,
            adult_male_count = adult_male_count,
            adult_female_count = adult_female_count,
            children_count = children_count,
            children_ages = children_ages,
            have_pets = have_pets,
            pets_description = pets_description,
            special_needs = special_needs,
            volunteer_note = volunteer_note,
            finance_status = finance_status,
            how_long_to_stay = how_long_to_stay,
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
