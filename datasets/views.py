from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .forms import DatasetModificationRequestForm
from .utils import run_scraper
from django.core.exceptions import ObjectDoesNotExist
from json import JSONDecodeError
from .utils import SCRAPER_MAPPING
from .forms import CollectionForm 
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from rest_framework import viewsets
from .serializers import DatasetSerializer, CleanedDatasetSerializer
import json
import logging
from .models import Dataset, ModificationRequest, Collection, Person
from .scraper.constants import scraper_constants

logger = logging.getLogger(__name__)

# -------
def modification_manager_check(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff or user.groups.filter(name='Modification Manager').exists())

def difa_admin(view_func):
    decorator = user_passes_test(
        modification_manager_check,
        login_url='datasets',
    )

    def _wrapped_view_func(request, *args, **kwargs):
        if not modification_manager_check(request.user):
            messages.error(request, "You are unauthorized to view that page!")
        return decorator(view_func)(request, *args, **kwargs)

    return _wrapped_view_func

# # ------------------------------------------------------------------------------------------
# # User authentication views
# # ------------------------------------------------------------------------------------------

from django.views.generic import TemplateView
from datasets.forms import UserProfileForm
from datasets.models import UserProfile
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from .forms import AccountSettingsForm

@method_decorator(login_required, name='dispatch')
class AccountSettingsView(FormView):
    template_name = 'datasets/account_settings.html'
    form_class = AccountSettingsForm
    success_url = '/configure_account/'

    def form_valid(self, form):
        # Process the form data here
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'], _ = UserProfile.objects.get_or_create(user=self.request.user)
        return context

@login_required
def complete_profile(request):
    user = request.user
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if profile is not None:
        return redirect('index') 

    if request.method == 'POST':
        if not profile:
            # Create a new profile only if it does not exist and the form is being submitted
            profile = UserProfile(user=user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()

    return render(request, 'datasets/complete_profile.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    print(profile)
    if request.method == 'POST':
        if not profile:
            profile = UserProfile(user=user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('configure_account') 
    else:
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()

    return render(request, 'datasets/update_profile.html', {'form': form})

@login_required
def change_name(request):
    user = request.user

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Name updated successfully.")
            return redirect('configure_account')  # Redirect to the account settings page or another appropriate page
    else:
        form = AccountSettingsForm(instance=user)

    return render(request, 'datasets/change_name.html', {'form': form})
# ------------------------------------------------------------------------------------------
# Dataset-related views
# ------------------------------------------------------------------------------------------
def datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/datasets.html', {'datasets': datasets})

def dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    return render(request, 'datasets/dataset.html', {'dataset': dataset, 'scraper_constants': scraper_constants})

class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class CleanedDatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = CleanedDatasetSerializer
    
@difa_admin
def scrape_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except ObjectDoesNotExist:
        messages.error(request, "Dataset does not exist!")
        return redirect('datasets')

    try:
        scraped_data = run_scraper(dataset_id)
        if scraped_data is None:
            messages.error(request, "An error occurred while scraping the dataset!")
            return redirect('datasets')

        # Update dataset with scraped data
        for key, value in scraped_data.items():
            setattr(dataset, key, value)
        dataset.last_scraped = timezone.now()
        dataset.is_errored = False
        dataset.save()
        messages.success(request, "Dataset scraped and updated successfully!")
    except Exception as e:
        logger.error("Error scraping dataset ID %s: %s", dataset_id, str(e), exc_info=True)
        messages.error(request, "An unexpected error occurred while scraping the dataset!")

    return redirect('dataset', dataset_id=dataset_id)

# ------------------------------------------------------------------------------------------
# Modifications Portal Views
# ------------------------------------------------------------------------------------------

@login_required
@difa_admin
def modification_requests(request):
    mod_requests = ModificationRequest.objects.all().order_by('-id')
    return render(request, 'datasets/modification_requests.html', {'mod_requests': mod_requests})

@login_required
def create_modification_request(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    if request.method == 'POST':
        form = DatasetModificationRequestForm(request.POST, dataset=dataset)
        if form.is_valid():
            try:
                # Read changes from the 'changes_json' field
                changes_json = request.POST['changes_json']
                changes_dict = json.loads(changes_json)

                # Check if there are any real changes
                no_changes = True
                for field, new_value in changes_dict.items():
                    current_value = getattr(dataset, field, '')
                    if current_value != new_value:
                        no_changes = False
                        break

                if no_changes:
                    messages.error(request, 'No changes detected. Please make some changes before submitting.')
                    return redirect('create_modification_request', dataset_id=dataset.id)

                # Create the modification request
                mod_request = ModificationRequest(
                    dataset=dataset,
                    user=request.user,
                    changes=json.dumps(changes_dict),
                )
                mod_request.save()
                messages.success(request, 'Modification request submitted successfully.')
                logger.info("Modification request created for dataset %s by user %s", dataset_id, request.user)
                return redirect('dataset', dataset_id=dataset.id)
            except Exception as e:
                logger.error("Error creating modification request: %s", str(e), exc_info=True)
                messages.error(request, 'An error occurred while creating the modification request.')
    else:
        form = DatasetModificationRequestForm(dataset=dataset)

    return render(request, 'datasets/create_modification_request.html', {'form': form, 'dataset': dataset})

@login_required
@difa_admin
def view_changes(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)
    dataset = mod_request.dataset
    try:
        changes = json.loads(mod_request.changes)
    except JSONDecodeError as e:
        changes = {}
        error_message = f"Invalid JSON data in changes field for modification request ID: {mod_request_id}. JSON data: {mod_request.changes}"
        logger.error(error_message, exc_info=True)  # Log the error along with traceback
        messages.warning(request, 'Invalid JSON data in changes field.')

    # Add current value to the changes dictionary
    for field, new_value in changes.items():
        current_value = getattr(dataset, field, '')
        changes[field] = {'new_value': new_value, 'current_value': current_value}

    return render(request, 'datasets/view_changes.html', {'mod_request': mod_request, 'changes': changes})

@login_required
@difa_admin
def approve_request(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)
    if mod_request.status != 'pending':
        messages.warning(request, "This modification request has already been reviewed.")
        return redirect('modification_requests')
  
    mod_request.status = 'approved'
    mod_request.approver = request.user
    mod_request.save()
    logger.info("Modification request %s approved by user %s", mod_request_id, request.user)
    messages.success(request, f'Modification request {mod_request.id} approved.')
    return redirect('modification_requests')

@login_required
@difa_admin
def reject_request(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)
    if mod_request.status != 'pending':
        messages.warning(request, "This modification request has already been reviewed.")
        return redirect('modification_requests')

    mod_request.status = 'rejected'
    mod_request.approver = request.user
    mod_request.save()
    messages.success(request, f'Modification request {mod_request.id} rejected.')
    return redirect('modification_requests')

@login_required
@difa_admin
def modify_modification_request(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'approved', 'rejected']:
            mod_request.status = new_status
            mod_request.approver = request.user
            mod_request.save()
            messages.success(request, f"Modification request status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status provided.")

    return redirect('view_changes', mod_request_id=mod_request.id)

@login_required
@difa_admin
def delete_modification_request(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, pk=mod_request_id)
    mod_request.delete()
    messages.success(request, 'Modification request deleted successfully.')
    return redirect('modification_requests')

class TncView(TemplateView):
    template_name = 'datasets/tnc.html'

# ------------------------------------------------------------------------------------------
# Collection Related Views
# ------------------------------------------------------------------------------------------
def collections(request):
    user_collections = Collection.objects.filter(user=request.user) if request.user.is_authenticated else None

    # Exclude user's collections from global_collections if user is authenticated
    if user_collections:
        global_collections = Collection.objects.exclude(user=request.user)
    else:
        global_collections = Collection.objects.all()

    form = CollectionForm()
    return render(request, 'datasets/collections.html', {
        'global_collections': global_collections,
        'user_collections': user_collections,
        'form': form
    })


@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            # Create a collection object without saving to the database
            new_collection = form.save(commit=False)
            new_collection.user = request.user
            new_collection.save()
            form.save_m2m()  # Save the many-to-many relationship (datasets)
            messages.success(request, 'Collection created successfully.')
            logger.info("Collection created by user %s", request.user)
        else:
            messages.error(request, 'There was an error creating the collection.')
            logger.warning("Error creating collection by user %s: %s", request.user, form.errors)

        return redirect('collections')
    else:
        return redirect('collections')

def collection(request, collection_id):
    try:
        # Fetch the specific collection using provided collection_id
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        messages.error(request, "The requested collection does not exist or you don't have permission to view it.")
        logger.warning("Collection with ID %s not found", collection_id)
        return redirect('collections')

    context = {'collection': collection}
    return render(request, 'datasets/collection.html', context)

# Search and Scrape Views
def searchpage(request):
    return render(request, 'datasets/searchpage.html')

def search_results(request):
    query = request.GET.get('q', '')
    context = {'query': query}
    return render(request, 'datasets/search_results.html', context)

scraping_progress = 0
current = ""

@difa_admin
@login_required
def scrape_all_view(request):
    # print(request.user.is_staff)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are unauthorized to scrape all datasets!")
        logger.warning("Unauthorized scrape attempt by user %s", request.user)
        return redirect('datasets')
    
    user_id = request.user.id
    # Initialize progress for this specific user
    request.session[f'scrape_progress_{user_id}'] = 0

    scraping_progress = 0
    for dataset_id in SCRAPER_MAPPING:
        ds = Dataset.objects.get(pk=dataset_id)
        # Use user-specific keys in the cache
        cache.set(f'scraping_progress_{user_id}', scraping_progress)
        cache.set(f'current_dataset_{user_id}', ds.dataset_name)
        
        # Try to scrape data for the dataset_id
        try:
            scraped_data = run_scraper(dataset_id)
        except Exception as e:
            # Log the actual exception details
            logger.error("Error scraping dataset_id %s: %s", dataset_id, e)
            messages.error(request, f"Internal Server Error occurred after updating {(scraping_progress)} datasets! Please try again later.")
            return redirect('datasets')

        # Add timestamp to scraped data
        scraped_data['last_scraped'] = timezone.now().isoformat()
        
        # Update the database with the scraped data
        for key, value in scraped_data.items():
            setattr(ds, key, value)
        
        ds.save()
        scraping_progress += 1

    messages.success(request, f"Scraped {(scraping_progress)} datasets successfully!")
    return redirect()

@difa_admin
def scraping_progress_view(request):
    user_id = request.user.id

    # Retrieve the scraping progress and current dataset from the cache using user-specific keys
    progress = cache.get(f'scraping_progress_{user_id}', 0)
    current_dataset = cache.get(f'current_dataset_{user_id}', '')

    # Return the progress, current dataset, and total count in JSON format
    return JsonResponse({'progress': progress, 'current': current_dataset, 'total': len(SCRAPER_MAPPING)})

@difa_admin
@login_required
def admin_page(request):
    return render(request, 'datasets/admin_page.html')


# ------------------------------------------------------------------------------------------
# Static Site Pages views
# ------------------------------------------------------------------------------------------
def workshop(request):
    day1_sessions = [
        {
            "start_time": "12:00pm",
            "end_time": "12:30pm",
            "duration": "30 minutes",
            "session": "Day 1 Opening Remarks",
            "description": "Greetings from the FAMPS and FSN Chairs",
            "youtube_link":"https://www.youtube.com/watch?v=cjhrjQTeaq0",
            "speakers": [12, 19]
        },
        {
            "start_time": "12:30pm",
            "end_time": "1:15pm",
            "duration": "45 minutes",
            "session": "Session 1",
            "description": "Why should we care about data linkages?",
            "youtube_link":"https://www.youtube.com/watch?v=NDuzX3wuIQw",
            "speakers": [2]
        },
        {
            "start_time": "1:15pm",
            "end_time": "2:00pm",
            "duration": "45 minutes",
            "session": "Keynote speaker",
            "description": "Methods for linking administrative data",
            "youtube_link":"https://www.youtube.com/watch?v=5jJfv0RzP44",
            "speakers": [1]
        },
        {
            "start_time": "2:15pm",
            "end_time": "2:45pm",
            "duration": "30 minutes",
            "session": "Session 2",
            "description": "Linking Administrative Data: The UMETRICS Experience",
            "youtube_link":"https://www.youtube.com/watch?v=p0lTVB4gQkE",
            "speakers": [3]
        },
        {
            "start_time":"2:45pm",
            "end_time":"3:00pm",
            "duration":"15 minutes",
            "session":"Break",
            "description":"Break",
            "speakers":[]
        },
        {
            "start_time": "3:00pm",
            "end_time": "3:45pm",
            "duration": "45 minutes",
            "session": "Session 3",
            "description": "Developments in data linkages",
            "youtube_link":"https://www.youtube.com/watch?v=-_zdr6SRAQU",
            "speakers": [20]
        },
        {
            "start_time": "3:45pm",
            "end_time": "4:15pm",
            "duration": "30 minutes",
            "session": "Session 4 (Research Presentations)",
            "youtube_link":"https://www.youtube.com/watch?v=bPcZ-QW78Pw",
            "description": "Frontiers in evidence-based policy making: COVID-19 and Schools",
            "speakers": [4]
        },
        {
            "start_time": "4:15pm",
            "end_time": "4:45pm",
            "duration": "30 minutes",
            "session": "Session 4 (Research Presentations)",
            "youtube_link":"https://www.youtube.com/watch?v=8Jw-jFjcFkE",
            "description": "Evidence on WIC using administrative data linkage",
            "speakers": [5]
        },
        {
            "start_time": "4:45pm",
            "end_time": "5:00pm",
            "duration": "15 minutes",
            "session": "Day 1 Wrap-up",
            "description": "Closing from the FAMPS and FSN Chairs; Preview of Day 2",
            "youtube_link":"#",
            "speakers": [12, 19]
        }
        ]
    day2_sessions = [
    {
        "start_time": "12:00pm",
        "end_time": "12:15pm",
        "duration": "15 minutes",
        "session": "Day 2 Opening Remarks",
        "description": "Greetings from the FAMPS and FSN Chairs; Highlights from Day 1",
        "youtube_link": "https://www.youtube.com/watch?v=ndiQmUUxi9k",
        "speakers": [12, 19]
    },
    {
        "start_time": "12:15pm",
        "end_time": "1:15pm",
        "duration": "60 minutes",
        "session": "Session 5",
        "description": "Challenges and bottlenecks of working with administrative data",
        "youtube_link": "https://www.youtube.com/watch?v=XWrJ4ewASqE",
        "speakers": [6, 7, 8, 9]
    },
    {
        "start_time": "1:15pm",
        "end_time": "1:35pm",
        "duration": "20 minutes",
        "session": "Session 6",
        "description": "Linking Administrative Data: The IPUMS Experience",
        "youtube_link": "https://www.youtube.com/watch?v=GRfKbc8fs40",
        "speakers": [10]
    },
    {
        "start_time": "1:35pm",
        "end_time": "2:05pm",
        "duration": "30 minutes",
        "session": "Session 7 (Research Presentations)",
        "description": "Policy Analysis at the Intersection of Constraints and Nutrition",
        "youtube_link": "https://www.youtube.com/watch?v=Vc4q-rcEOS4",
        "speakers": [21]
    },
    {
        "start_time": "2:05pm",
        "end_time": "2:35pm",
        "duration": "30 minutes",
        "session": "Session 7 (Research Presentations)",
        "description": "Aggregate Conditions, Child Growth, & the DHS",
        "youtube_link": "https://www.youtube.com/watch?v=Gh2Gv24yp44",
        "speakers": [11]
    },
    {
        "start_time": "2:35pm",
        "end_time": "2:50pm",
        "duration": "15 minutes",
        "session": "Break",
        "description": "Break",
        "speakers": []
    },
    {
        "start_time": "2:50pm",
        "end_time": "3:30pm",
        "duration": "40 minutes",
        "session": "Activity 3",
        "description": "Deterministic Data Linkages: Matching and Fuzzy Matching",
        "youtube_link": "https://www.youtube.com/watch?v=_yIWVTy-72k",
        "speakers": [12]
    },
    {
        "start_time": "3:30pm",
        "end_time": "4:10pm",
        "duration": "40 minutes",
        "session": "Activity 2",
        "description": "Data quality: Considerations when using linked data",
        "youtube_link": "https://www.youtube.com/watch?v=poUAfpXeefA",
        "speakers": [18]
    },
    {
        "start_time": "4:10pm",
        "end_time": "4:50pm",
        "duration": "40 minutes",
        "session": "Activity 1",
        "description": "Navigating Licenses and Building a Research Plan to Access RDC Data",
        "youtube_link": "https://www.youtube.com/watch?v=kN0pyEv3t3E",
        "speakers": [19]
    },
    {
        "start_time": "4:50pm",
        "end_time": "5:00pm",
        "duration": "10 minutes",
        "session": "Day 2 Wrap-up",
        "description": "Closing from the FAMPS and FSN Chairs",
        "youtube_link": "https://www.youtube.com/watch?v=0zEtZ6092IQ",
        "speakers": [12, 19]
    }
]

    return render(request, 'datasets/workshop.html', context={"day1_sessions":day1_sessions, "day2_sessions":day2_sessions})

def partners(request):
    return render(request, 'datasets/partners.html')

def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    if person.image:
        person_image_url = person.image.url
    else:
        person_image_url = None

    if person.presentation_slides:
        presentation_slides_url = person.presentation_slides.url
    else:
        presentation_slides_url = None

    context = {
        'person_name': person.name,
        'person_image': person_image_url,
        'person_description': person.description,
        'difa_workshop_presentation': person.difa_workshop_presentation or None,
        'presentation_slides': presentation_slides_url,
        'more_information': person.more_information or None,
    }
    return render(request, 'datasets/person_template.html', context)

def research_team(request):
    first_people_ids = [22, 23]
    first_people = [Person.objects.get(pk=person_id) for person_id in first_people_ids]
    remaining_people = Person.objects.filter(team='research').exclude(id__in=first_people_ids).order_by('name')
    research_team_members = list(first_people) + list(remaining_people)

    context = {
        'research_team_members': research_team_members,
    }
    return render(request, 'datasets/research_team.html', context)


def leadership_team(request):
    leadership_team_members = Person.objects.filter(team='leadership')
    first_people_ids = [12,19]
     # Query the people with the specified IDs and order them according to the list.
    first_people = [Person.objects.get(pk=person_id) for person_id in first_people_ids]

    # Query the remaining people and order them by name (or any other field you prefer).
    remaining_people = Person.objects.filter(team='leadership').exclude(id__in=first_people_ids).order_by('name')

    # Combine the two querysets.
    leadership_team_members = list(first_people) + list(remaining_people)

    context = {
        'team_members': leadership_team_members,
    }
    return render(request, 'datasets/leadership_team.html', context)

def about(request):
    return render(request, 'datasets/about.html')