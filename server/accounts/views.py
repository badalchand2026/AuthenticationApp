
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminRole





# Register

class RegisterAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "User registered successfully.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# Login
class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "success": True,
                    "message": "Login successful.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role
                    },
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# Logout
class LogoutAPIView(APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message": "Logout successful."
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or blacklisted refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# Profile

class ProfileAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response(
            {
                "success": True,
                "message": "Profile retrieved successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role
                }
            },

            status=status.HTTP_200_OK
        )





# Admin Dashboard

class AdminDashboardAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminRole]

    def get(self, request):

        return Response(
            {
                "success": True,
                "message": "Welcome to the Admin Dashboard.",
                "admin": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "role": request.user.role
                }
            },
            status=status.HTTP_200_OK
        )
