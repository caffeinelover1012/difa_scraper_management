from django.contrib import admin

# Register your models here.
from .models import Dataset, Collection, ModificationRequest

admin.site.register(Dataset)
admin.site.register(Collection)
admin.site.register(ModificationRequest)
