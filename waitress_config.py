from waitress import serve
from difa_scraper_management.wsgi import application  # Update this import based on your Django project's structure

if __name__ == "__main__":
    serve(application, host='127.0.0.1', port=8000)
