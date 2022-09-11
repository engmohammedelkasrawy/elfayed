# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib import messages
# from django.contrib.auth.models import User
# from .models import Student


# @receiver(post_save, sender=User)
# def post_save_create_student(created, sender, instance, *args, **kwargs):
#     if created:
#         Student.objects.create(user=instance)
