from django.contrib import admin
from .models import DataifaUser, UserProfile, Dataset, Collection, ModificationRequest, Person, VerificationQuestion

# Inline admin for Verification Questions
class VerificationQuestionInline(admin.TabularInline):
    model = VerificationQuestion
    fields = ('question', 'answer')  # Specify the fields to display
    extra = 0  # Removes extra empty fields

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, VerificationQuestionInline)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile', )
    ordering = ('email',)

# Unregister the old user admin and register the new one with the UserProfile
if admin.site.is_registered(DataifaUser):
    admin.site.unregister(DataifaUser)
admin.site.register(DataifaUser, UserAdmin)

# Register other models
admin.site.register(Dataset)
admin.site.register(Collection)
admin.site.register(ModificationRequest)
admin.site.register(Person)
