from rest_framework import serializers

from users.models import User, Friends


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)


class SearchUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["public_id", "name", "email"]


class RequestSerializer(serializers.Serializer):
    REQUEST_STATE = (
        ("send", "send"),
        ("accepted", "accepted"),
        ("reject", "reject"),
    )
    state = serializers.ChoiceField(choices=REQUEST_STATE)


class FriendListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="receiver.name")
    public_id = serializers.CharField(source="receiver.public_id")

    class Meta:
        model = Friends
        fields = ["name", "public_id"]
