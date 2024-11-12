from sqlalchemy import select

from src.contacts.models import Contact
from src.contacts.schema import ContactCreate, ContactUpdate


class ContactRepository:

    def __init__(self, session):
        self.session = session

    async def get_contacts(self, skip: int = 0, limit: int = 10) -> list[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_contact(self, contact_id: int) -> Contact:

        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate) -> Contact:
        new_contact = Contact(**contact.model_dump())
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)  # To get the ID from the database
        return new_contact

    async def update_contact(
        self, contact_id: int, contact_update: ContactUpdate
    ) -> Contact:
        contact = await self.get_contact(contact_id)
        if contact:
            for key, value in contact_update.model_dump().items():
                setattr(contact, key, value)
            await self.session.commit()
            await self.session.refresh(contact)

        return contact

    async def search_contacts(self, query):
        q = select(Contact).filter(
            (Contact.first_name.ilike(query))
            | (Contact.last_name.ilike(query))
            | (Contact.email.ilike(query))
        )
        results = await self.session.execute(q)
        return results.scalars().all()

    async def delete_contact(self, contact_id: int):
        q = select(Contact).filter(Contact.id == contact_id)
        result = await self.session.execute(q)
        contact = result.scalar_one()
        await self.session.delete(contact)
        await self.session.commit()
