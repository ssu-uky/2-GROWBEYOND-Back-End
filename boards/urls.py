from django.urls import path
from . import views

urlpatterns = [
    path("write/", views.PossibleBoardWrite.as_view()),
    path("detail/<int:post_pk>/", views.PossibleBoardDetail.as_view()),
]
