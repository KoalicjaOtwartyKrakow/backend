from utils.db import DB
from utils.orm import Guest


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
        )
        session.add(guest)
        session.commit()
        session.refresh(guest)
        assert guest.claimed_by_id is None
        assert guest.claimed_at is None

        guest.claimed_by_id = "782962fc-dc11-4a33-8f08-b7da532dd40d"
        session.commit()
        session.refresh(guest)

        assert str(guest.claimed_by_id) == "782962fc-dc11-4a33-8f08-b7da532dd40d"
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
