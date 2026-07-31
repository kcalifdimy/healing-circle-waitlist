import json
import logging
import re

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# Same intent as the client-side check: "something@something.tld".
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@ensure_csrf_cookie
def index(request):
    """Serve the landing page (the View + Template of MVT)."""
    return render(request, "waitlist/index.html")


@require_POST
def join_waitlist(request):
    """
    Receive {"email": "..."} from the waitlist form and forward it
    to the site owner's inbox (settings.WAITLIST_NOTIFY_EMAIL).
    """
    # Accept JSON (what the page's fetch() sends) or normal form data.
    if request.content_type == "application/json":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
        email = str(payload.get("email", "")).strip()
    else:
        email = request.POST.get("email", "").strip()

    if not EMAIL_RE.match(email):
        return JsonResponse(
            {"ok": False, "error": "Please provide a valid email address."},
            status=400,
        )

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M UTC")
    subject = "New Healing Circle waitlist signup"
    message = (
        "Someone just joined the Healing Circle waitlist.\n\n"
        f"Email:  {email}\n"
        f"Time:   {timestamp}\n"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.WAITLIST_NOTIFY_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send waitlist notification email")
        return JsonResponse(
            {"ok": False, "error": "Could not process signup right now."},
            status=502,
        )

    return JsonResponse({"ok": True})
