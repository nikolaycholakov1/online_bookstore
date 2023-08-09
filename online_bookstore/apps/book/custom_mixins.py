from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy


class AnonymousRequiredMixin(UserPassesTestMixin, AccessMixin):
    """
    Mixin ensures that authenticated users get redirected.
    """

    request: HttpRequest

    def test_func(self):
        return not self.request.user.is_authenticated

    # URL to redirect to if the user is authenticated
    login_url = reverse_lazy('home-page')

    # Overriding this method to redirect instead of raising a Forbidden error.
    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())
