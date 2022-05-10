import pytest

from users import models
from posts import models as p_models
from auth import hashing


@pytest.fixture(autouse=True)
def create_fake_user(tmpdir):
    """Fixture to execute asserts before and after a test is run"""

    from database.test_db import override_get_db

    database = next(override_get_db())
    new_user = models.Users(
        username="Samuraii", email="test@gmail.com", password=hashing.get_password_hash("password"), is_stuff=True
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    yield

    database.query(models.Users).delete()
    database.commit()
