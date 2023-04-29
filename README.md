# DIFA Scraper Management

This project simplifies the management and running process of various scrapers and datasets using a Django web application. Users can log in, register, create modification requests, and manage datasets based on permissions.

## Tools Used

- Python
- Django 
- Web Scraping (BeautifulSoup4, Selenium)
- Frontend (Bootstrap, HTML, CSS, JS)

## Python Version

Python 3.8 or higher is recommended for this project.

## Installation

Follow the steps below to install and set up the project on your local machine:

1. Clone the repository:
```
git clone https://github.com/caffeinelover1012/difa_scraper_management.git
cd difa-scraper-management
```


2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate
```

3. Install the required packages:

```
pip install -r requirements.txt

```

4. Navigate to the directory where manage.py is present.
Apply migrations to set up the database:

```
python manage.py makemigrations
python manage.py migrate

```
5. Run the server
```
python manage.py runserver

```
