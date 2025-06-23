import pytest
from django.contrib.auth.models import User
import tempfile
import shutil
import pytest
from django.conf import settings


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='fixtureuser', password='pass')


@pytest.fixture(autouse=True, scope='session')
def temp_media_root(tmp_path_factory):
    tmp_media = tmp_path_factory.mktemp('media')
    settings.MEDIA_ROOT = str(tmp_media)
    yield
    shutil.rmtree(str(tmp_media), ignore_errors=True)

