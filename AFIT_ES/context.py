from event.models import Category, Event

def context(request):
    event = Event.objects.all().order_by('-created')
    category = Category.objects.all()
    context = {
        'categories' : category,
        'events': event
    }
    return context