import requests
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication,
    TokenMatchesOASRequirements,
)
from oauth2_provider.models import Application
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import PublicId
from social_app.settings import HOSTNAME
from users.models import User, Friends
from users.serializers import (
    UserSignUpSerializer,
    UserLoginSerializer,
    SearchUserListSerializer,
    RequestSerializer,
    FriendListSerializer,
)
from users.utils import validate_pagination


class UserSignUpView(APIView):
    """
    This class is used to create user.
    """

    @staticmethod
    def post(request):
        """
        @param request:
        @return return success response with 201 status code.
        """
        try:
            serial_data = UserSignUpSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                email = serial_data.validated_data["email"]
                user = User.objects.create(
                    email=email, username=email, public_id=PublicId.create_public_id()
                )
                user.set_password(serial_data.validated_data["password"])
                user.save()
                return Response(
                    {"message": "SignUp successfully.", "public_id": user.public_id},
                    status.HTTP_201_CREATED,
                )
        except IntegrityError:
            return Response(
                {"error": "Email already exists."}, status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(APIView):
    """
    This class is used to create access token for authenticate user.
    """

    def post(self, request):
        """
        @param request:
        @return return access token for authenticate user.
        """
        serial_data = UserLoginSerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            email = serial_data.validated_data["email"]
            password = serial_data.validated_data["password"]
            if User.objects.filter(email=email).exists():
                auth_user = authenticate(username=email, password=password)
                if auth_user is None:
                    return Response(
                        {"error": "Invalid Credentials."}, status.HTTP_400_BAD_REQUEST
                    )
                auth_user = User.objects.get(email=email)
                app = Application()
                client_secret = app.client_secret
                client_id = app.client_id
                app.authorization_grant_type = "password"
                app.client_type = "client-credentials"
                app.redirect_uris = request.build_absolute_uri("/")
                app.save()
                auth_data = {
                    "username": auth_user.username,
                    "password": password,
                    "grant_type": "password",
                    "client_id": client_id,
                    "client_secret": client_secret,
                }
                token = requests.post(
                    HOSTNAME + "/o/token/",
                    data=auth_data,
                ).json()

                token["public_id"] = auth_user.public_id
                return Response(token)
            return Response({"error": "Email not found."}, status.HTTP_400_BAD_REQUEST)


class SearchUserView(APIView):
    def get(self, request):
        # TODO API to search other users by email and name(paginate up to 10 records per page).API to search other
        #  users by email and name(paginate up to 10 records per page). TODO Before the run this endpoint,
        #   You need to create user data by python shell or other way, because you don't mention any type of user
        #   creations things.

        """
        @param request:
        @return: Return search result list with 200 status code.
        """
        limit, offset = validate_pagination(request)
        users = User.objects.filter(
            Q(email__iexact=request.GET.get("search"))
            | Q(name__icontains=request.GET.get("search"))
        )[offset:limit]
        user_list = SearchUserListSerializer(users, many=True).data
        return Response(user_list)


class RequestManageView(APIView):
    """
    This class is used to send friend request.
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "POST": [["create"]],
    }

    @method_decorator(csrf_exempt)
    @method_decorator(ratelimit(key='user', rate='3/m', block=True))
    def post(self, request, public_id):
        """
        @param public_id: user public id to find which you want to send friend request.
        @param request:
        @return: Success response with 200 status code.
        """
        try:
            serial_data = RequestSerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                state = serial_data.validated_data["state"]
                receiver = User.objects.get(public_id=public_id)
                if receiver.public_id == request.user.public_id:
                    return Response(
                        {"error": "You cannot send a friend request to yourself"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if state == "send":
                    if Friends.objects.filter(
                            sender=request.user, receiver=receiver, request_state="send"
                    ).exists():
                        return Response(
                            {"error": "Friend request already sent"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    Friends.objects.create(
                        sender=request.user,
                        receiver=receiver,
                        public_id=PublicId.create_public_id(),
                        request_state=state,
                    )
                    return Response({"message": "Request send successfully."})

                elif state == "reject":
                    Friends.objects.filter(
                        sender=request.user,
                        receiver=receiver,
                    ).delete()
                    return Response({"message": "Request rejected."})

                elif state == "accepted":
                    if Friends.objects.filter(
                            user=request.user, friend=receiver, request_state="accepted"
                    ).exists():
                        return Response(
                            {"error": "You are already friends"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    friend = Friends.objects.get(
                        sender=request.user,
                        receiver=receiver,
                    )
                    friend.request_state = "accepted"
                    friend.save()
                    return Response({"message": "Request accepted."})

        except User.DoesNotExist:
            return Response(
                {"error": "User not found. Please choose correct id"},
                status.HTTP_404_NOT_FOUND,
            )


class FriendsView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "GET": [["read"]],
    }

    def get(self, request):
        return Response(
            FriendListSerializer(
                Friends.objects.filter(sender=request.user, request_state="accepted"),
                many=True,
            ).data
        )


class PendingFriendsView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenMatchesOASRequirements]

    required_alternate_scopes = {
        "GET": [["read"]],
    }

    def get(self, request):
        return Response(
            FriendListSerializer(
                Friends.objects.filter(sender=request.user, request_state="send"),
                many=True,
            ).data
        )
