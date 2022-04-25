import pytest
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_continuum.utils import count_versions

from kokon.orm import Guest
from kokon.utils.db import DB

from tests.helpers import admin_session


def test_app_user():
    with admin_session() as session:
        session.execute("TRUNCATE guests_version RESTART IDENTITY;")
        session.execute("TRUNCATE guests RESTART IDENTITY;")
        session.execute("TRUNCATE transaction RESTART IDENTITY;")

    with DB().acquire() as session:
        # creates a guest without error and version as well
        guid = "74b86069-c837-4431-a7ee-3a4aedda978b"

        guest = Guest(
            guid=guid,
            full_name="John Smith",
            email="john.smith@yahoo.com",
            phone_number="100-330-497",
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
        # trigger works
        claimed_at = guest.claimed_at
        assert claimed_at is not None

        guest.adult_male_count = 1
        session.commit()

        with pytest.raises(ProgrammingError):
            _ = guest.versions[0]

    with admin_session() as session:
        guest = session.query(Guest).where(Guest.guid == guid).one()
        assert count_versions(guest) == 2
        assert str(guest.versions[0].guid) == guid
