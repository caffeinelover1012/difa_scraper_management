from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class DataifaUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=20, blank=True, null=True, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.display_name:
            return self.display_name
        return 'User'
    
    @property
    def get_level(self):
        if self.is_superuser:
            return "Superuser"
        elif self.is_staff:
            return "DIFA Admin"
        elif self.profile.is_verified:
            return "Verified DIFA User"
        elif not self.profile.is_verified and self.is_active:
            return "Unverified DIFA User"
        else:
            return "Unregistered"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])  # like "Andrew E"
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'User'
        self.display_name = dn.strip()

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.email,)

class VerificationQuestion(models.Model):
    VERIFICATION_QUESTIONS = [
        ('childhood_nickname', 'What was your childhood nickname?'),
        ('favorite_childhood_friend', 'What is the name of your favorite childhood friend?'),
        ('parents_meet_city', 'In what city or town did your mother and father meet?'),
        ('favorite_team', 'What is your favorite team?'),
        ('dream_job_child', 'What was your dream job as a child?'),
        ('first_car_make_model', 'What was the make and model of your first car?'),
        ('hospital_born', 'What was the name of the hospital where you were born?'),
        ('childhood_sports_hero', 'Who is your childhood sports hero?'),
        ('mothers_maiden_name', 'What was your mother’s maiden name?'),
    ]

    user = models.ForeignKey(DataifaUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, choices=VERIFICATION_QUESTIONS)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.get_question_display()  

class UserProfile(models.Model):
    """Profile data about a user."""

    user = models.OneToOneField(DataifaUser, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    institution_employer_name = models.CharField(max_length=100, blank=True, verbose_name="Institution/Employer Name")
    institution_personal_website = models.CharField(max_length=256,blank=True, null=True)
    occupation_category = models.CharField(max_length=100, blank=True)
    occupation_title = models.CharField(max_length=100, blank=True)
    field_of_research = models.CharField(max_length=100, blank=True)
    research_areas = models.CharField(max_length=255, blank=True)
    general_research_statement = models.TextField(blank=True)
    how_did_you_learn = models.CharField(max_length=255, blank=True, verbose_name='How did you learn about DIFA?')
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")

    def __str__(self):
        return str(self.user.email)

    class Meta():
        db_table = 'user_profile'

@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    # preferred_avatar_size_pixels = 256

    # picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
    #     hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
    #     preferred_avatar_size_pixels
    # )
    if sociallogin:
        # print(sociallogin.account.extra_data)
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'google':
            # print(sociallogin.account.extra_data)
            user.first_name = sociallogin.account.extra_data['given_name']
            if sociallogin.account.extra_data.get('family_name'):
                user.last_name = sociallogin.account.extra_data['family_name']
            else:
                user.last_name = ""
            user.is_verified=True
            # verified = sociallogin.account.extra_data['verified_email']
            picture_url = sociallogin.account.extra_data['picture']

    user.guess_display_name()
    user.save()

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=700)
    about_info = models.TextField(blank=True)
    last_updated = models.CharField(max_length=255, blank=True)
    dataset_file_format = models.CharField(max_length=1024, blank=True)
    dataset_status = models.CharField(max_length=255, blank=True)
    sponsor_name = models.CharField(max_length=700, blank=True)
    access_type = models.CharField(max_length=255, blank=True)
    dataset_link = models.CharField(max_length=700, blank=True)
    dataset_website_link = models.CharField(max_length=700, blank=True)
    dataset_citation = models.TextField(blank=True)
    dataset_collection_method = models.TextField(blank=True)
    last_scraped = models.CharField(max_length=255, blank=True)
    other_info = models.TextField(blank=True)
    is_errored = models.BooleanField(default=False)

    def __str__(self):
        return self.dataset_name

class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), null=True,on_delete=models.SET_NULL)
    datasets = models.ManyToManyField(Dataset, related_name='related_collections', related_query_name='collection')

    def __str__(self):
        return self.name

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
    user = models.ForeignKey(get_user_model(),null=True, on_delete=models.SET_NULL, related_name='modification_requests')
    changes = models.TextField(blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)
    approver = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='approver_mod_requests')

    def __str__(self):
        return f'Modification Request {self.id} - {self.dataset.dataset_name} - {self.user.email}'

class Person(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='persons/images/')
    description = models.TextField()
    difa_workshop_presentation = models.URLField(null=True, blank=True)
    presentation_slides = models.FileField(upload_to='persons/presentation_slides/',blank=True, null=True)
    more_information = models.URLField(blank=True)
    TEAM_CHOICES = [
        ('leadership', 'Leadership Team'),
        ('research', 'Research Team'),
        ('guest', 'Guest'),
    ]
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, default='guest')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
