from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = CICharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = CIEmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=255)
    about_info = models.TextField(blank=True)
    last_updated = models.CharField(max_length=255, blank=True)
    dataset_file_format = models.CharField(max_length=255, blank=True)
    dataset_status = models.CharField(max_length=255, blank=True)
    sponsor_name = models.CharField(max_length=255, blank=True)
    access_type = models.CharField(max_length=255, blank=True)
    dataset_link = models.CharField(max_length=255, blank=True)
    dataset_website_link = models.CharField(max_length=255, blank=True)
    dataset_citation = models.TextField(blank=True)
    dataset_collection_method = models.TextField(blank=True)
    last_scraped = models.CharField(max_length=255, blank=True)
    other_info = models.TextField(blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, related_name='datasets')

    def __str__(self):
        return self.dataset_name


class ModificationRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]


    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='modification_requests')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='modification_requests')
    changes = models.TextField(blank=True)  # You can use a JSONField if you want to store changes as JSON
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Modification Request {self.id} - {self.dataset.dataset_name} - {self.user.username}'
