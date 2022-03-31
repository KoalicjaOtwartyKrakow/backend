import enum


# https://stackoverflow.com/a/51976841
class VerificationStatus(str, enum.Enum):
    """Class representing verification status enum in database."""

    CREATED = "CREATED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

    def __str__(self):
        return self.value


class WorkflowStatus(str, enum.Enum):
    """Class representing workflow status enum in database."""

    AVAILABLE = "AVAILABLE"
    NEEDS_VERIFICATION = "NEEDS_VERIFICATION"
    WITHDRAWN = "WITHDRAWN"
    DONE = "DONE"


# https://stackoverflow.com/a/51976841
class GuestPriorityStatus(str, enum.Enum):
    """Class representing status enum in database."""

    DOES_NOT_RESPOND = "DOES_NOT_RESPOND"
    ACCOMMODATION_NOT_NEEDED = "ACCOMMODATION_NOT_NEEDED"
    EN_ROUTE_UA = "EN_ROUTE_UA"
    EN_ROUTE_PL = "EN_ROUTE_PL"
    IN_KRK = "IN_KRK"
    AT_R3 = "AT_R3"
    ACCOMMODATION_FOUND = "ACCOMMODATION_FOUND"
    UPDATED = "UPDATED"

    def __str__(self):
        return self.value


# https://stackoverflow.com/a/51976841
class Voivodeship(str, enum.Enum):
    """Class representing voivodeship enum in database."""

    DOLNOSLASKIE = "DOLNOŚLĄSKIE"
    KUJAWSKOPOMORSKIE = "KUJAWSKO-POMORSKIE"
    LUBELSKIE = "LUBELSKIE"
    LUBUSKIE = "LUBUSKIE"
    LODZKIE = "ŁÓDZKIE"
    MALOPOLSKIE = "MAŁOPOLSKIE"
    MAZOWIECKIE = "MAZOWIECKIE"
    OPOLSKIE = "OPOLSKIE"
    PODKARPACKIE = "PODKARPACKIE"
    PODLASKIE = "PODLASKIE"
    POMORSKIE = "POMORSKIE"
    SLASKIE = "ŚLĄSKIE"
    SWIETOKRZYSKIE = "ŚWIĘTOKRZYSKIE"
    WARMINSKOMAZURSKIE = "WARMIŃSKO-MAZURSKIE"
    WIELKOPOLSKIE = "WIELKOPOLSKIE"
    ZACHODNIOPOMORSKIE = "ZACHODNIOPOMORSKIE"


class LanguageEnum(enum.Enum):
    """Class representing language enum in database."""

    ENGLISH = "En"
    POLISH = "Pl"
    UKRAINIAN = "Uk"
    RUSSIAN = "Ru"
