from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(OtpResetPassword)
admin.site.register(Watched)


class RegisterVideodmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(RegisterVideo,RegisterVideodmin)