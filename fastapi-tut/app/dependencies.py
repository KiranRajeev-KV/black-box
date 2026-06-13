import sqlite3
from typing import Annotated, Generator, Protocol

from fastapi import Depends, Query

from app.models import UserCreate
from app.repositories.users import UserRepository

from app.database import db_connection

# protocol means any class with the same methods satify type checking as UserRepository
# eg:- both user_repository (this is a module/file with multiple functions) and FakeUserRepository (this is a class with the methods)
# but both works because each python module is imported as an object with methods and attributes.

# so the definition of protocol here is 
# Any object that has a callable create_user() returning dict is acceptable.

# the common name for this is called duck typing.
# if module/class/object has the method/function i need, i will use it.

# i will be moving to a wrapper class for the user repository as thats a good practice
class UserRepositoryProtocol(Protocol):
    def create_user(self, user: UserCreate) -> dict:
        ...
    def list_users(self) -> list[dict]:
        ...


def get_user_repository() -> UserRepositoryProtocol:
    return UserRepository()
    
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


# query param dependancy
def get_pagination(
    # offset: int = Query(default=0, ge=0),
    # limit: int = Query(default=10, ge=1, le=100),
    
    # modern FastAPI prefered way
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict:
    return {
        "offset": offset,
        "limit": limit,
    }

PaginationDep = Annotated[dict, Depends(get_pagination)]


# yield dep
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    with db_connection() as connection:
        yield connection


DbConnectionDep = Annotated[sqlite3.Connection, Depends(get_db_connection)]

    

