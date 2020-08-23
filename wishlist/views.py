from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from family.models import Family
from family.views import GetUserFamilyMixin


class WishlistView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)
        context = {}
        family: Family
        try:
            wishlist = defaultdict(list)
            for wish in family.wish_set.all():
                print(wish.title)
                wishlist[f'{wish.user.username} ({wish.user.first_name} {wish.user.last_name})'].append(wish)

            wishlist = list(wishlist.items())
            print(wishlist)
            context['wishlist'] = wishlist
        except Exception:
            context['wishlist'] = None

        context['family'] = family

        return render(request, 'wishlist.html', context)

