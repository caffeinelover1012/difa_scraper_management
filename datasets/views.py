from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import Dataset
from .utils import run_scraper
from django.utils import timezone

def index(request):
    return render(request, 'datasets/index.html')

@login_required
def scrape_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    scraper_id = dataset.scraper_id
    scraped_data = run_scraper(scraper_id)
    # Update the 'last_scraped' attribute with the current date and time
    scraped_data['last_scraped'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

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
