import os
import sys

import pytest
from django.contrib.auth.models import User
from django.test import Client

from family.models import Family
from family.tests.test_utils import create_fake_user, create_fake_family, create_fake_gallery
from gallery.models import Gallery


@pytest.fixture
def client():
    """Client for testing purposes"""
    client = Client()
    return client


@pytest.fixture
def set_up():
    """Populate the database"""
    u1 = create_fake_user('jonaszkofta')
    f1 = create_fake_family('Kowalski', 'kowalski')
    f2 = create_fake_family('Hopps', 'hopps')
    g1 = create_fake_gallery('m', f1, True)
    g2 = create_fake_gallery('m', f2, True)

    f1.user.add(u1)
    f1.gallery_set.add(g1)
    f2.user.add(u1)
    f2.gallery_set.add(g2)
    f1.save()
    f2.save()

    return u1


