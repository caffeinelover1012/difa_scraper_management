from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, RegistrationForm, DatasetModificationRequestForm
from .models import Dataset, ModificationRequest, Collection
from .utils import run_scraper
import json
from json import JSONDecodeError


def index(request):
    return render(request, 'datasets/index.html')


# User authentication views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'datasets/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
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
@login_required
def datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/datasets.html', {'datasets': datasets})


@login_required
def dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    return render(request, 'datasets/dataset.html', {'dataset': dataset})


def scrape_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
        scraped_data = run_scraper(dataset_id)

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
    
@login_required
def export_dataset(request, dataset_id):
    # export dataset to Google Sheets
    export_successful = True   
    # redirect back to dataset page with success or error message
    if export_successful:
        messages.success(request, 'Dataset exported successfully.')
    else:
        messages.error(request, 'Failed to export dataset.')

    return redirect('dataset', dataset_id=dataset_id)


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

from .forms import CollectionForm  # Add this import

@login_required
def collections(request):
    collections = Collection.objects.filter(user=request.user)
    form = CollectionForm()  # Create an instance of the form
    return render(request, 'datasets/collections.html', {'collections': collections, 'form': form})  # Pass the form to the context


@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            new_collection = form.save(commit=False)
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


@login_required
def collection(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
    except Collection.DoesNotExist:
        messages.error(request, "The requested collection does not exist or you don't have permission to view it.")
        return redirect('collections')

    context = {
        'collection': collection,
    }
    return render(request, 'datasets/collection.html', context)
