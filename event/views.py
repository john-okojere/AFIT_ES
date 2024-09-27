from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EventForm, TicketForm
from .models import Category, Event, Ticket
from django.http import JsonResponse
from django.db.models import Q


def home(request):
    locations = Event.objects.values_list('location', flat=True).distinct()
    return render(request, 'event/index.html',{'locations': locations,})

def detail(request, uid):
    event = Event.objects.get(uid=uid)
    events = Event.objects.filter(category = event.category)
    return render(request, 'event/detail.html', {'event':event, 'events':events})

from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Event

def all(request):
    # Check if it's an AJAX request by inspecting the request header
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_query = request.GET.get('search_query', '').strip()
        search_location = request.GET.get('search_location', '').strip()

        # Start with a basic queryset of all events
        events = Event.objects.all().order_by('-created')

        # Apply search filters based on input
        if search_query:
            events = events.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) | 
                Q(category__name__icontains=search_query)
            )
        
        if search_location:
            events = events.filter(location__icontains=search_location)

        # Prepare data to return as JSON
        event_data = []
        for event in events:
            event_data.append({
                'uid': str(event.uid),  # Ensure UUID is serialized as a string
                'title': event.title,
                'location': event.location,
                'created': event.created.strftime('%Y-%m-%d %H:%M:%S'),
                'image_url': event.image.url if event.image else '',  # Use event image URL or empty string if no image
            })

        return JsonResponse({'events': event_data})
    search_query = request.GET.get('search_query', '').strip()
    search_location = request.GET.get('search_location', '').strip()
    if search_query or search_location:
         # Apply search filters based on input
        events = Event.objects.all().order_by('-created')
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )
    
        events = events.filter(location__icontains=search_location)

        # Prepare data to return as JSON
        event_data = []
        for event in events:
            event_data.append({
                'uid': str(event.uid),  # Ensure UUID is serialized as a string
                'title': event.title,
                'location': event.location,
                'created': event.created.strftime('%Y-%m-%d %H:%M:%S'),
                'image_url': event.image.url if event.image else '',  # Use event image URL or empty string if no image
            })
    # For non-AJAX requests (normal page load)
    events = Event.objects.all().order_by('-created')
    paginator = Paginator(events, 16)  # Show 16 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get distinct locations for the filter dropdown
    locations = Event.objects.values_list('location', flat=True).distinct()

    context = {
        'events': page_obj,
        'locations': locations,
    }
    return render(request, 'event/all.html', context)


def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()

            # Check the event type and handle ticket creation
            if event.type == 'Free Event':
                # Create a default ticket for free events
                Ticket.objects.create(
                    event=event,
                    ticket_name='Free Ticket',
                    ticket_price=0
                )
            elif event.type == 'Ticketed Event':
                # Handle ticket creation for ticketed events
                ticket_names = request.POST.getlist('ticket_name')
                ticket_prices = request.POST.getlist('ticket_price')
                for name, price in zip(ticket_names, ticket_prices):
                    if name and price:
                        Ticket.objects.create(
                            event=event,
                            ticket_name=name,
                            ticket_price=float(price)  # Ensure price is treated as float
                        )

            return redirect('/')
    else:
        form = EventForm()

    context = {
        'form': form,
    }
    return render(request, 'event/create.html', context)