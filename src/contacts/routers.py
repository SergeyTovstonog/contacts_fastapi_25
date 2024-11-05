from fastapi import APIRouter, Query, Path

from src.contacts.schema import Contact, ContactResponse

router = APIRouter()

@router.get("/contact/all")
async def get_contact(skip: int = None, limit: int = Query(default=10, le=100, ge=10)):
    return {"contacts": f"all contacts, skip - {skip}, limit - {limit}"}

@router.post("/contact")
async def create_contact(contact: Contact) -> ContactResponse:
    return ContactResponse(first_name=contact.first_name, last_name=contact.last)

@router.get("/contact/{contact_id}")
async def get_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0, le=10)):
    return {"contact_id": contact_id}