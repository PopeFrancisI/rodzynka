import pytest
from django.urls import reverse


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
    response = client.get(reverse('family_main', args=('kowalski', )), follow=True)
    assert response.status_code == 200
