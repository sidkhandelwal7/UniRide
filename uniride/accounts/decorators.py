from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache


def verified_required(view):
    """
    Use this on every page for posting, searching for, or joining rides.

    - Visitors who are not signed in are sent to the sign-in page (US19).
    - Signed-in students who have not verified their Pitt email are sent to a
      page that asks them to verify first (US2).
    - never_cache tells the browser not to keep a copy of the page, so after
      signing out the back button cannot show it again (US19).
    """

    @wraps(view)
    def check_verified(request, *args, **kwargs):
        if not request.user.is_verified:
            return redirect("accounts:verify_first")
        return view(request, *args, **kwargs)

    return never_cache(login_required(check_verified))
