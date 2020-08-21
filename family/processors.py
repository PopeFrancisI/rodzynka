from django.contrib.auth.models import AnonymousUser

from family.models import Family


def header_data(request):
    context = {}
    if request.session.get('current_family_slug'):
        context['current_family'] = request.user.family_set.get(slug=request.session.get('current_family_slug'))
    if not request.user.is_anonymous:
        user_families = Family.objects.filter(user=request.user)
        context['user_families'] = user_families
    return context
