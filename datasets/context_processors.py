from .models import Person

def persons(request):
    persons_list = Person.objects.filter(show=True)
    return {'persons': persons_list}
