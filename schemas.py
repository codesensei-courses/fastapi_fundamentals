from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        """Setting the passwords actually sets password_hash."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash."""
        return pwd_context.verify(password, self.password_hash)


class TripInput(SQLModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class Trip(TripInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []

