from .models import Dataset, Collection, ModificationRequest, Person, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name')  # add other fields if you want

if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.register(get_user_model(), UserAdmin)


admin.site.register(Dataset)
admin.site.register(Collection)
admin.site.register(ModificationRequest)
admin.site.register(Person)
