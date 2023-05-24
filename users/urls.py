from django.urls import path

from users.views import (
    UserSignUpView,
    UserLoginView,
    SearchUserView,
    RequestManageView,
    FriendsView, PendingFriendsView,
)

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    # API to search other users by email and name(paginate up to 10 records per page).
    path("search_user/", SearchUserView.as_view(), name="search-view"),
    # • API to send/accept/reject friend request
    path(
        "request_state/<int:public_id>/",
        RequestManageView.as_view(),
        name="send-friend-request",
    ),
    # API to list friends(list of users who have accepted friend request)
    path(
        "friends/",
        FriendsView.as_view(),
        name="friend-list",
    ),

    # List pending friend requests(received friend request)
    path(
        "pending_request/",
        PendingFriendsView.as_view(),
        name="pending-friend-list",
    ),
]
