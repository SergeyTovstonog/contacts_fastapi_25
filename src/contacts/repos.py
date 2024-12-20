from fastapi_cache.decorator import cache
from sqlalchemy import select

from config.cache import custom_repo_key_builder
from src.contacts.models import Contact
from src.contacts.schema import ContactCreate, ContactUpdate


class ContactRepository:

    def __init__(self, session):
        self.session = session

    @cache(expire=600, namespace="get_contacts_repo", key_builder=custom_repo_key_builder)
    async def get_contacts(
        self, owner_id: int, skip: int = 0, limit: int = 10
    ) -> list[Contact]:
        query = (
            select(Contact)
            .where(Contact.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_contact(self, contact_id: int, owner_id: int) -> Contact:
        query = select(Contact).where(
            Contact.id == contact_id, Contact.owner_id == owner_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate, owner_id: int) -> Contact:
        new_contact = Contact(**contact.model_dump(), owner_id=owner_id)
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)  # To get the ID from the database
        return new_contact

    async def update_contact(
        self, contact_id: int, contact_update: ContactUpdate, owner_id: int
    ) -> Contact:
        contact = await self.get_contact(contact_id, owner_id)
        if contact:
            for key, value in contact_update.model_dump().items():
                setattr(contact, key, value)
            await self.session.commit()
            await self.session.refresh(contact)

        return contact

    async def search_contacts(self, query: str, owner_id: int):
        q = (
            select(Contact)
            .filter(Contact.owner_id == owner_id)
            .filter(
                (Contact.first_name.ilike(query))
                | (Contact.last_name.ilike(query))
                | (Contact.email.ilike(query))
            )
        )
        results = await self.session.execute(q)
        return results.scalars().all()

    async def delete_contact(self, contact_id: int, owner_id: int):
        q = (
            select(Contact)
            .filter(Contact.id == contact_id)
            .filter(Contact.owner_id == owner_id)
        )
        result = await self.session.execute(q)
        contact = result.scalar_one()
        await self.session.delete(contact)
        await self.session.commit()

    async def get_contacts_all(self, limit: int = 10, offset: int = 0):
        query = select(Contact).offset(offset).limit(limit)
        results = await self.session.execute(query)
        return results.scalars().all()
