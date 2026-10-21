from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that exempts API endpoints from CSRF enforcement,
    allowing seamless session-based API interactions from React and cURL.
    """

    def enforce_csrf(self, request):
        return  # Bypass CSRF check for REST API calls
