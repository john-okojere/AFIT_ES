from event.models import Category

def context(request):
    category = Category.objects.all()
    context = {
        'categories' : category
    }
    return context