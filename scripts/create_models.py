import sys

# I have no idea how python modules work
sys.path.append("..")
sys.path.append("../..")
from backend.utils.db import get_engine
from backend.utils.orm import Base


if __name__ == "__main__":
    Base.metadata.create_all(get_engine())
