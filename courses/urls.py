from django.urls import path
from . import views
urlpatterns = [
    path("register_videos", views.register_videos, name="register_videos"),
    path("lesson/<int:branch_id>/<int:lesson_id>", views.lesson, name="lesson")
]

