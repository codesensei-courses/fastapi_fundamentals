"""
create_user.py
-------------
A convenience script to create a user.
"""

from getpass import getpass

from sqlmodel import SQLModel, Session, create_engine

from schemas import User


engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True # Log generated SQL
)


if __name__ == "__main__":
    print("Creating tables (if necessary)")
    SQLModel.metadata.create_all(engine)

    print("--------")

    print("This script will create a user and save it in the database.")

    username = input("Please enter username\n")
    pwd = getpass("Please enter password\n")

    with Session(engine) as session:
        user = User(username=username)
        user.set_password(pwd)
        session.add(user)
        session.commit()
