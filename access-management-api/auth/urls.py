from django.urls import path

from .views import GroupAddAPIView, GroupRemoveAPIView, LoginAPIView, UserMeAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('group/<str:type>/add/', GroupAddAPIView.as_view(), name='group-add'),
    path('group/<str:type>/remove/', GroupRemoveAPIView.as_view(), name='group-remove'),
    path('user/me/', UserMeAPIView.as_view(), name='user-me'),
]
