import pytest
from django.test import Client

from tests.test_utils import create_fake_user, create_fake_family, create_fake_gallery, create_fake_calendar, \
    create_fake_wish


@pytest.fixture
def client():
    """Client for testing purposes"""
    client = Client()
    return client


@pytest.fixture
def set_up():
    """Populate the database"""
    u1 = create_fake_user('jonaszkofta')
    u2 = create_fake_user('jolalojalna')

    f1 = create_fake_family('Kowalski', 'kowalski')
    f2 = create_fake_family('Hopps', 'hopps')

    g1 = create_fake_gallery('m', f1, True)
    g2 = create_fake_gallery('m', f2, True)

    f1.user.add(u1)
    f1.gallery_set.add(g1)
    create_fake_calendar('mc', f1, True)
    create_fake_wish('zebranie', 'dawdwa', True, f1, u1)
    create_fake_wish('spacer', 'po Łazienkach', False, f1, u2)

    f2.user.add(u1)
    f2.user.add(u2)
    f2.gallery_set.add(g2)
    create_fake_calendar('mc', f2, True)

    f1.save()
    f2.save()

    return u1


