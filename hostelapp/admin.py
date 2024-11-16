from django.contrib import admin

from hostelapp import models

# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Hostel)
admin.site.register(models.food)
admin.site.register(models.Warden)