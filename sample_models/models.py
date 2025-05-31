from typing import Any

from sqlalchemy import Column, Integer, String

from sample_models import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"<User {self.name}>"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


# class Org(Base):
#     """
#     dasda
#     """

#     __tablename__ = "org"
#     id: int = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
#     name: str = Column(String(50), nullable=False)
#     public_id: uuid.UUID = Column(UUID, nullable=False, unique=True)

#     def __init__(self, name, public_id):
#         self.name = name
#         self.public_id = public_id
