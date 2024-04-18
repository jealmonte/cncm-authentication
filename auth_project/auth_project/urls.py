from django.urls import path, include
from auth_app.views import SignupView, LoginView, UserDetailsView, UpdateUserProfileView, DeleteUserView, UserListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('update-profile/<int:pk>/', UpdateUserProfileView.as_view(), name='update-profile'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('users/', UserListView.as_view(), name='user-list'),
]