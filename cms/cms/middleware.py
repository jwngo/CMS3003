from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path_info).url_name

        url_is_exempt = url_name in settings.LOGIN_EXEMPT_URLS

        if url_name == 'user_logout':
            logout(request)

        if request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL + "?next=" + request.path_info)