from django.urls import path
from . import views
urlpatterns = [
    path("quiz/<int:id>", views.quiz, name="quiz"),
    path("result", views.result, name="result")
]
