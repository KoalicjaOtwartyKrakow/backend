from utils.db import DB

from .accommodations import AccommodationsRepo
from .guests import GuestsRepo
from .hosts import HostsRepo
from .users import UsersRepo


class Repos:
    def __init__(self):
        db = DB()

        self.accommodations = AccommodationsRepo(db)
        self.guests = GuestsRepo(db)
        self.hosts = HostsRepo(db)
        self.users = UsersRepo(db)

        self.db = db
