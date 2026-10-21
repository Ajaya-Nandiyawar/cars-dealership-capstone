import json
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    """
    POST /api/auth/register/
    Accepts: username, first_name, last_name, email, password
    """

    def post(self, request):
        data = request.data
        username = (data.get("username") or data.get("userName") or "").strip()
        first_name = (data.get("first_name") or data.get("firstName") or "").strip()
        last_name = (data.get("last_name") or data.get("lastName") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        # Validate required fields
        missing = []
        if not username:
            missing.append("username")
        if not first_name:
            missing.append("first_name")
        if not last_name:
            missing.append("last_name")
        if not email:
            missing.append("email")
        if not password:
            missing.append("password")

        if missing:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Email format validation
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            return Response(
                {"error": "Invalid email address format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Password length validation
        if len(password) < 6:
            return Response(
                {"error": "Password must be at least 6 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Duplicate username check
        if User.objects.filter(username__iexact=username).exists():
            return Response(
                {"error": "Username already exists. Please choose a different username."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Duplicate email check
        if User.objects.filter(email__iexact=email).exists():
            return Response(
                {"error": "Email is already registered. Please use another email or log in."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user with Django's secure password hashing
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return Response(
            {
                "status": "success",
                "message": "User registered successfully.",
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    """
    POST /api/auth/login/
    Accepts: username, password
    Authenticates user and starts a Django session.
    """

    def post(self, request):
        data = request.data
        username = (data.get("username") or data.get("userName") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return Response(
                {"error": "Both username and password are required.", "status": "Failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {"error": "User account is disabled.", "status": "Failed"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            login(request, user)
            return Response(
                {
                    "status": "Authenticated",
                    "userName": user.username,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "isStaff": user.is_staff,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid username or password.", "status": "Failed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Terminates current user session.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Access underlying request for session termination
        req = getattr(request, "_request", request)
        username = req.user.username if hasattr(req, "user") and req.user.is_authenticated else ""
        logout(req)
        return Response(
            {
                "status": "success",
                "message": f"User {username} logged out successfully." if username else "Logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        req = getattr(request, "_request", request)
        logout(req)
        return Response(
            {"status": "success", "message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    """
    GET /api/auth/me/
    Returns current authenticated user details or unauthenticated status.
    """

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "authenticated": True,
                    "userName": request.user.username,
                    "username": request.user.username,
                    "firstName": request.user.first_name,
                    "lastName": request.user.last_name,
                    "email": request.user.email,
                    "isStaff": request.user.is_staff,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"authenticated": False, "userName": None},
            status=status.HTTP_200_OK,
        )
