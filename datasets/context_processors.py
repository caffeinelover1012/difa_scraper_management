from .models import Person

def persons(request):
    persons_list = Person.objects.filter(show=True)
    guest_persons_list = Person.objects.filter(show=True, team='guest')
    return {'persons': persons_list, 'guest_persons': guest_persons_list}
