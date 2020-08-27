import pytest
from django.urls import reverse

from family.models import Family
from gallery.models import Gallery


@pytest.mark.django_db
def test_get_family_pick(client, set_up):
    client.login(username='jonaszkofta', password='testpass123')

    response = client.get(reverse('family_pick'), follow=True)
    assert response.status_code == 200

    user_families = set_up.family_set.all()
    assert len(response.context['user_families']) == len(user_families)


@pytest.mark.django_db
def test_get_family_main(client, set_up):
    client.login(username='jonaszkofta', password='testpass123')

    response = client.get(reverse('family_main', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    user_families = set_up.family_set.all()
    assert len(response.context['user_families']) == len(user_families)


@pytest.mark.django_db
def test_get_family_calendar(client, set_up):
    """first gets to main page, then to calendar page"""
    client.login(username='jonaszkofta', password='testpass123')

    response = client.get(reverse('family_main', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    response = client.get(reverse('calendar_detail', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    assert response.context['current_calendar'].is_main
    assert response.context['current_calendar'].family.slug == 'kowalski'


@pytest.mark.django_db
def test_add_event(client, set_up):
    test_get_family_main(client, set_up)

    main_calendar = Family.objects.get(slug='kowalski').calendar_set.get(is_main=True)
    year = 2020
    month = 8
    day = 20
    response = client.get(reverse('event_create', args=('kowalski', main_calendar.id, year, month, day)),
                          follow=True)
    assert response.status_code == 200

    number_of_events_before = Family.objects.get(slug='kowalski').calendar_set.get(is_main=True).event_set.count()
    response = client.post(reverse('event_create', args=('kowalski', main_calendar.id, year, month, day)),
                           {
                               'title': 'new_event',
                               'description': 'blabla',
                               'is_important': True,
                               'time': '12:15'
                           },
                           follow=True)
    assert response.status_code == 200
    assert Family.objects.get(slug='kowalski') \
               .calendar_set.get(is_main=True).event_set.count() == number_of_events_before + 1
    assert Family.objects.get(slug='kowalski').calendar_set.get(is_main=True).event_set.get(id=1).title == 'new_event'


@pytest.mark.django_db
def test_get_family_gallery_pick(client, set_up):
    test_get_family_main(client, set_up)

    response = client.get(reverse('gallery_pick', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    main_gallery = Gallery.objects.get(family=Family.objects.get(slug='kowalski'))
    assert main_gallery in response.context['galleries'][0]


@pytest.mark.django_db
def test_get_family_gallery_main(client, set_up):
    test_get_family_main(client, set_up)

    response = client.get(reverse('gallery_pick', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    main_gallery = Gallery.objects.get(family=Family.objects.get(slug='kowalski'), is_main=True)
    response = client.get(reverse('gallery_detail', args=('kowalski', main_gallery.id)), follow=True)
    assert response.status_code == 200
    assert response.context['gallery'] == main_gallery


@pytest.mark.django_db
def test_get_family_wishlist(client, set_up):
    test_get_family_main(client, set_up)

    response = client.get(reverse('wishlist', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    assert len(response.context['wishlist']) == 2

    assert len(response.context['wishlist'][0][1]) == 1


@pytest.mark.django_db
def test_add_wish(client, set_up):
    test_get_family_main(client, set_up)

    response = client.get(reverse('wish_create', args=('kowalski',)), follow=True)
    assert response.status_code == 200

    number_of_wishes_before = Family.objects.get(slug='kowalski').wish_set.count()
    response = client.post(reverse('wish_create', args=('kowalski',)),
                           {
                               'title': 'new_wish',
                               'description': 'blabla',
                               'is_important': True
                           },
                           follow=True)
    assert response.status_code == 200
    assert Family.objects.get(slug='kowalski').wish_set.count() == number_of_wishes_before + 1
