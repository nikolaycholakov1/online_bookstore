from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy


class AnonymousRequiredMixin(UserPassesTestMixin, AccessMixin):
    request: HttpRequest

    def test_func(self):
        return not self.request.user.is_authenticated

    # URL to redirect to if the user is authenticated
    login_url = reverse_lazy('home-page')

    # Overriding this method to redirect instead of raising a Forbidden error.
    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())


class CustomPermissionDeniedMixin:
    NO_ACCESS_TEMPLATE = 'error_pages/no-access.html'
    NO_ACCESS_ERROR_MSG = 'You are not allowed to access this page.'

    def handle_no_permission(self):
        # Retrieve the error message; if not set in the view, use the default one from the mixin.
        error_message = getattr(self, 'NO_ACCESS_ERROR_MSG', self.NO_ACCESS_ERROR_MSG)

        context = {
            'error_message': error_message
        }
        return render(self.request, self.NO_ACCESS_TEMPLATE, context)
