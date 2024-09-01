from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EventForm, TicketForm
from .models import Category, Event, Ticket


def home(request):
    return render(request, 'event/index.html')

def detail(request, uid):
    event = Event.objects.get(uid=uid)
    return render(request, 'event/detail.html', {'event':event})



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