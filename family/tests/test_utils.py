from django.contrib.auth.models import User
from faker import Faker

from family.models import Family
from gallery.models import create_gallery

fake = Faker('pl_PL')


def create_fake_user(username):
   user = User.objects.create(
        username=username,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email()
    )
   user.set_password('testpass123')
   user.save()
   return user


def create_fake_family(name, slug):
    return Family.objects.create(
        name=name,
        last_name=fake.first_name(),
        slug=slug
    )


def create_fake_gallery(name, family, is_main):
    return create_gallery(name, family, is_main)

