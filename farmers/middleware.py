import time
from django.contrib.auth import logout
from django.shortcuts import redirect

IDLE_TIMEOUT = 10 * 60
class InactivityLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = time.time()
            last_activity = request.session.get("last_activity")

            if last_activity is not None:
                if now - last_activity > IDLE_TIMEOUT:
                    logout(request)
                    return redirect("login")

            # Record the time of this request
            request.session["last_activity"] = now

        return self.get_response(request)