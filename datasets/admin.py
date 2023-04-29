from django.contrib import admin

# Register your models here.
from .models import Dataset, Collection, ModificationRequest, User, Person
from django.contrib.auth.admin import UserAdmin


admin.site.register(Dataset)
admin.site.register(Collection)
admin.site.register(ModificationRequest)
admin.site.register(User,UserAdmin)
admin.site.register(Person)
