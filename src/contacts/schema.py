from datetime import date

from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: str | None = None


class ContactResponse(Contact):
    id: int

    class Config:
        from_attributes = True


class ContactCreate(Contact):
    pass


class ContactUpdate(Contact):
    pass
