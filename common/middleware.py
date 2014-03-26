from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class LoginRequiredMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated() and not "/admin" in request.path_info:
            return HttpResponseRedirect(reverse('admin:index'))
