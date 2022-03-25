from sqlalchemy_continuum.utils import count_versions

from utils.db import DB
from utils.orm import AccommodationUnit, Guest


def test_guests_claimed_at(db):
    with DB().acquire() as session:
        guest = Guest(
            guid="5e42beb8-00a8-4577-8d2b-8ae29257a424",
            full_name="Marta Andrzejak",
            email="auz-oxloij-dxfv@yahoo.com",
            phone_number="499-330-497",
            people_in_group=4,
            adult_male_count=0,
            adult_female_count=2,
            children_ages=[1, 10],
            have_pets=False,
            how_long_to_stay="1w",
            updated_by_id="782962fc-dc11-4a33-8f08-b7da532dd40d",
        )
        session.add(guest)
        session.commit()
        session.refresh(guest)
        assert guest.claimed_by_id is None
        claimed_at = guest.claimed_at
        assert claimed_at is not None

        guest.claimed_by_id = "782962fc-dc11-4a33-8f08-b7da532dd40d"
        session.commit()
        session.refresh(guest)

        assert str(guest.claimed_by_id) == "782962fc-dc11-4a33-8f08-b7da532dd40d"
        assert guest.claimed_at > claimed_at
        claimed_at = guest.claimed_at
        assert claimed_at

        # edit another field
        guest.email = "auz-oxloij-another@yahoo.com"
        session.commit()
        session.refresh(guest)

        assert guest.claimed_at == claimed_at

        # edit claimed_by_id to null
        guest.claimed_by_id = None
        session.commit()
        session.refresh(guest)

        assert guest.claimed_at > claimed_at


def test_versioning(db):
    with DB().acquire() as session:
        guest = Guest(
            guid="5e42beb8-00a8-4577-8d2b-8ae29257a424",
            full_name="Marta Andrzejak",
            email="auz-oxloij-dxfv@yahoo.com",
            phone_number="499-330-497",
            children_ages=[1, 10],
            updated_by_id="782962fc-dc11-4a33-8f08-b7da532dd40d",
        )
        session.add(guest)
        session.commit()
        session.refresh(guest)

        assert count_versions(guest) == 1

        accommodation_unit = AccommodationUnit(
            address_line="ul. Zimna 19m.28",
            city="Lublin",
            zip="06-631",
            voivodeship="LUBELSKIE",
            vacancies_total=5,
            vacancies_free=5,
            host_id="2078dad6-5dc9-4e5a-8ee0-d69c44f460e2",
        )

        guest.accommodation_unit = accommodation_unit
        guest.email = "email.1@yahoo.com"
        session.commit()
        session.refresh(guest)

        assert count_versions(guest) == 2
        assert guest.versions[0].email == "auz-oxloij-dxfv@yahoo.com"

        # accommodation change does not create a new guest version
        # but any change in guest will use the latest accommodation version
        guest.accommodation_unit.city = "Warsaw"
        guest.email = "email.2@yahoo.com"
        session.commit()
        session.refresh(guest)

        assert count_versions(guest) == 3
        assert guest.versions[0].accommodation_unit is None
        assert guest.versions[1].accommodation_unit.city == "Lublin"
        assert guest.versions[2].accommodation_unit.city == "Warsaw"
