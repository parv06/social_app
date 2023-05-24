from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Friends(BaseModel):
    class Meta:
        db_table = "friends"

    REQUEST_STATE = (
        ("send", "send"),
        ("accepted", "accepted"),
        ("reject", "reject"),
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_friend_requests"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_friend_requests"
    )
    request_state = models.CharField(choices=REQUEST_STATE, max_length=20)
