from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import Dataset
from .utils import run_scraper
from django.utils import timezone
from .models import ModificationRequest

def index(request):
    return render(request, 'datasets/index.html')

def export_dataset(request, dataset_id):
    # export dataset to Google Sheets
    export_successful=True   
    # redirect back to dataset page with success or error message
    if export_successful:
        messages.success(request, 'Dataset exported successfully.')
    else:
        messages.error(request, 'Failed to export dataset.')

    return redirect('dataset', dataset_id=dataset_id)
@login_required
def modification_requests(request):
    mod_requests = ModificationRequest.objects.all().order_by('-id')
    return render(request, 'datasets/modification_requests.html', {'mod_requests': mod_requests})

def scrape_dataset(request, dataset_id):
    dataset, created = Dataset.objects.get_or_create(pk=dataset_id)
    scraped_data = run_scraper(dataset_id)

    # Update the 'last_scraped' attribute with the current date and time
    scraped_data['last_scraped'] = timezone.now().isoformat()

    # Update the database with the scraped data
    for key, value in scraped_data.items():
        setattr(dataset, key, value)
    dataset.save()

    return redirect('dataset', dataset_id=dataset.id)

@login_required
def datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/datasets.html', {'datasets': datasets})

@login_required
def dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    return render(request, 'datasets/dataset.html', {'dataset': dataset})

def user_login(request):
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
