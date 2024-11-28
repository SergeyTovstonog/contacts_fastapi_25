import pytest

from src.auth.models import Role

@pytest.mark.asyncio
async def test_register_user(user_role: Role, override_get_db):

    print(f"user_role: {user_role.id}, {user_role.name}")