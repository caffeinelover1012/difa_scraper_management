from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, RegistrationForm, DatasetModificationRequestForm
from .models import Dataset, ModificationRequest, Collection, Person
from .utils import run_scraper
import json
from django.core.exceptions import ObjectDoesNotExist
from json import JSONDecodeError
from .utils import SCRAPER_MAPPING
from .forms import CollectionForm 
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache

# def index(request):
#     return render(request, 'datasets/index.html')

# User authentication views
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'search')  # get the 'next' parameter, if it doesn't exist, default to 'search'
                print(next_url)
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'datasets/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'datasets/register.html', {'form': form, 'errors': form.errors, 'messages': messages.get_messages(request)})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


# Dataset-related views
def datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/datasets.html', {'datasets': datasets})


def dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    return render(request, 'datasets/dataset.html', {'dataset': dataset})

@login_required
def scrape_dataset(request, dataset_id):
    try:
        try:
            dataset = Dataset.objects.get(pk=dataset_id)
        except ObjectDoesNotExist:
            if SCRAPER_MAPPING.get(dataset_id) is None:
                    messages.error(request, "Invalid ID or Dataset does not exist!")
                    return redirect('datasets')
            dataset = Dataset.objects.create(pk=dataset_id)
        scraped_data = run_scraper(dataset_id)
        # print("here: ", dataset,dataset is None)
        # print(scraped_data)
        # Update the 'last_scraped' attribute with the current date and time
        scraped_data['last_scraped'] = timezone.now().isoformat()

        # Update the database with the scraped data
        for key, value in scraped_data.items():
            setattr(dataset, key, value)
        dataset.save()
        return redirect('dataset', dataset_id=dataset.id)
    except:
        messages.error(request, "Invalid ID or Dataset does not exist!")
        return redirect('datasets')
    

def modification_manager_check(user):
    return user.groups.filter(name='Modification Manager').exists()

@login_required
def create_modification_request(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    if request.method == 'POST':
        form = DatasetModificationRequestForm(request.POST, dataset=dataset)
        if form.is_valid():
            # Read changes from the 'changes_json' field
            changes_json = request.POST['changes_json']
            changes_dict = json.loads(changes_json)

            mod_request = ModificationRequest(
                dataset=dataset,
                user=request.user,
                changes=json.dumps(changes_dict),
            )
            mod_request.save()
            messages.success(request, 'Modification request submitted successfully.')
            return redirect('dataset', dataset_id=dataset.id)
    else:
        form = DatasetModificationRequestForm(dataset=dataset)

    return render(request, 'datasets/create_modification_request.html', {'form': form, 'dataset': dataset})


@login_required
def modification_requests(request):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, "You are unauthorized to view that page!")
        return redirect(datasets)
    mod_requests = ModificationRequest.objects.all().order_by('-id')
    return render(request, 'datasets/modification_requests.html', {'mod_requests': mod_requests})

@login_required
def view_changes(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)
    dataset = mod_request.dataset
    try:
        changes = json.loads(mod_request.changes)
    except JSONDecodeError:
        changes = {}
        messages.warning(request, 'Invalid JSON data in changes field.')
    
    # Add current value to the changes dictionary
    for field, new_value in changes.items():
        current_value = getattr(dataset, field, '')
        changes[field] = {'new_value': new_value, 'current_value': current_value}

    return render(request, 'datasets/view_changes.html', {'mod_request': mod_request, 'changes': changes})

@login_required
def approve_request(request, mod_request_id):
    if not any("ModificationManagers" in str(group) for group in request.user.groups.all()):
        messages.error(request, "You don't have permission to approve or reject modification requests.")
        return redirect('modification_requests')
    mod_request = get_object_or_404(ModificationRequest, id=mod_request_id)
    if mod_request.status != 'pending':
        messages.warning(request, "This modification request has already been reviewed.")
        return redirect('modification_requests')
  
    mod_request.status = 'approved'
    mod_request.approver = request.user
    mod_request.save()
    messages.success(request, f'Modification request {mod_request.id} approved.')
    return redirect('modification_requests')

@login_required
def reject_request(request, mod_request_id):
    if not any("ModificationManagers" in str(group) for group in request.user.groups.all()):
        messages.error(request, "You don't have permission to approve or reject modification requests.")
        return redirect('modification_requests')
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
def modify_modification_request(request, mod_request_id):
    if not any("ModificationManagers" in str(group) for group in request.user.groups.all()):
        messages.error(request, "You don't have permission to modify modification requests.")
        return redirect('modification_requests')

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
def delete_modification_request(request, mod_request_id):
    mod_request = get_object_or_404(ModificationRequest, pk=mod_request_id)
    mod_request.delete()
    messages.success(request, 'Modification request deleted successfully.')
    return redirect('modification_requests')


def collections(request):
    collections = Collection.objects.all()
    form = CollectionForm()  # Create an instance of the form
    return render(request, 'datasets/collections.html', {'collections': collections, 'form': form})  # Pass the form to the context


@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            new_collection = form.save(commit=False)
            # print('here')
            # print(new_collection)
            new_collection.user = request.user
            new_collection.save()
            form.save_m2m()  # Save the many-to-many relationship (datasets)
            messages.success(request, 'Collection created successfully.')
            return redirect('collections')
        else:
            messages.error(request, 'There was an error creating the collection.')
            return redirect('collections')
    else:
        return redirect('collections')


def collection(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        messages.error(request, "The requested collection does not exist or you don't have permission to view it.")
        return redirect('collections')

    context = {
        'collection': collection,
    }
    return render(request, 'datasets/collection.html', context)



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
    research_team_members = Person.objects.filter(team='research')
    context = {
        'research_team_members': research_team_members,
    }
    # print(SCRAPER_MAPPING)
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


def searchpage(request):
    return render(request, 'datasets/searchpage.html')

def search_results(request):
    query = request.GET.get('q', '')
    context = {'query': query}
    return render(request, 'datasets/search_results.html', context)

def datasets_json(request):
    data = serializers.serialize('json', Dataset.objects.all())
    return JsonResponse(data, safe=False)


scraping_progress=0
current=""
def scrape_all_view(request):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, "You are unauthorized to scrape all datasets!")
        return HttpResponse('Please Log In as an authorized user!', status=401)
    scraping_progress=0
    for dataset_id in SCRAPER_MAPPING:
        ds = Dataset.objects.get(pk=dataset_id)
        cache.set('scraping_progress', scraping_progress)
        cache.set('current_dataset', ds.dataset_name)
        scraped_data = run_scraper(dataset_id)
        # print("here: ", dataset,dataset is None)
        # print(scraped_data)
        # Update the 'last_scraped' attribute with the current date and time
        scraped_data['last_scraped'] = timezone.now().isoformat()
        # Update the database with the scraped data
        for key, value in scraped_data.items():
            setattr(ds, key, value)
        ds.save()
        scraping_progress+=1
    messages.success(f"Scraped {len(SCRAPER_MAPPING)} datasets successfully!")
    return redirect(datasets)

def scraping_progress_view(request):
    # Get the progress from the database or cache
    progress = cache.get('scraping_progress', 0)
    current_dataset = cache.get('current_dataset', '')
    return JsonResponse({'progress': progress,'current': current_dataset, 'total':len(SCRAPER_MAPPING)})


# def scrape_progress_view(request):
#     progress = get_scraping_progress()  # replace with your actual function
#     return JsonResponse({'progress': progress})
