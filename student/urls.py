from django.urls import path
from . import views
urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("student_info", views.student_info, name="student_info"),
    path("login_user", views.login_user, name="login_user"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("register_user", views.register_user, name="register_user"),
    path("off_videos", views.off_videos, name="off_videos"),
    path("on_videos", views.on_videos, name="on_videos"),
    path("quizzes", views.quizzes, name="quizzes"),
    path("quiz_result", views.quiz_result, name="quiz_result"),
    path("ask_reset_password", views.ask_reset_password, name="ask_reset_password"),
    path("get_otp", views.get_otp, name="get_otp"),
    path("set_new_password/<int:otp>",views.set_new_password, name="set_new_password"),
]


