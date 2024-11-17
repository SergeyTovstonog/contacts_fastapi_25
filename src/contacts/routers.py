from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.auth.models import User
from src.auth.schemas import RoleEnum
from src.auth.utils import get_current_user, RoleChecker
from src.contacts.repos import ContactRepository
from src.contacts.schema import Contact, ContactCreate, ContactResponse, ContactUpdate

router = APIRouter()

# @router.get("/contact/all")
# async def get_contact(skip: int = None, limit: int = Query(default=10, le=100, ge=10)):
#     return {"contacts": f"all contacts, skip - {skip}, limit - {limit}"}
#
# @router.post("/contact")
# async def create_contact(contact: Contact) -> ContactResponse:
#     return ContactResponse(first_name=contact.first_name, last_name=contact.last)


@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    contact_repo = ContactRepository(db)
    return await contact_repo.create_contact(contact, user.id)


@router.get(
    "/",
    response_model=list[ContactResponse],
)
async def get_contacts(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(RoleChecker([RoleEnum.USER])),
    db: AsyncSession = Depends(get_db),
):
    contact_repo = ContactRepository(db)
    return await contact_repo.get_contacts(user.id, skip, limit)


@router.get("/search", response_model=list[ContactResponse])
async def search_contacts(
    q: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(RoleChecker([RoleEnum.USER])),
):

    contact_repo = ContactRepository(db)
    return await contact_repo.search_contacts(q, user.id)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(RoleChecker([RoleEnum.USER])),
):

    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id, user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    user: User = Depends(RoleChecker([RoleEnum.USER])),
    db: AsyncSession = Depends(get_db),
):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id, user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return await contact_repo.update_contact(contact_id, contact_update)


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(RoleChecker([RoleEnum.USER])),
):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id, user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    await contact_repo.delete_contact(contact_id)
    return {"detail": "Contact deleted"}


@router.get(
    "/all/",
    response_model=list[ContactResponse],
    dependencies=[Depends(RoleChecker([RoleEnum.ADMIN]))],
    tags=["admin"],
)
async def get_all_contacts(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    contact_repo = ContactRepository(db)
    return await contact_repo.get_contacts_all(skip, limit)
