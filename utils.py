from django.shortcuts import redirect
from django.urls import reverse_lazy


def redirect_to_error_page(issue):
    return redirect(reverse_lazy('something_gone_wrong'),
                    args=(issue, ))
