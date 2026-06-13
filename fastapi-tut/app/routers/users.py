from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from app.models import UserCreate, UserPatch, UserPublic, UserUpdate
from app.repositories import users as user_repository
from app.dependencies import PaginationDep, UserRepositoryDep


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
def create_user(user: UserCreate, repo: UserRepositoryDep):
    return repo.create_user(user)


@router.get("", response_model=list[UserPublic])
# here the PaginationDep takes query parameter limit and offset
# GET /users?limit=10&limit=10
# this gets injected in to PaginationDep and calls pagination(limit=10, offset=10) and returns
# { "limit":10, "offset": 10 }

# why do this?
# extract repeated request concerns into dependencies, not random helper functions, 
# and FastAPI should parse/validate request data for them.
def list_users(repo: UserRepositoryDep, pagination: PaginationDep ):
    users = repo.list_users()

    offset = pagination["offset"]
    limit = pagination["limit"]

    return users[offset : offset + limit]


@router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(user_id: int):
    user = user_repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, updated_user: UserUpdate):
    user = user_repository.update_user(user_id, updated_user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.patch("/{user_id}", response_model=UserPublic)
def patch_user(user_id: int, user_patch: UserPatch):
    user = user_repository.patch_user(user_id, user_patch)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete("/{user_id}", response_model=UserPublic)
def delete_user(user_id: int):
    user = user_repository.delete_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user