from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EventForm
from .models import Category


def home(request):
    return render(request, 'event/index.html')

def detail(request):
    return render(request, 'event/detail.html')

def create(request):
    step = int(request.GET.get('step', 1))
    if 'event_data' not in request.session:
        request.session['event_data'] = {}

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                request.session['event_data'][key] = value

            if step < 4:
                return redirect(f'?step={step + 1}')
            else:
                event_data = request.session.pop('event_data')
                form = EventForm(event_data)
                if form.is_valid():
                    form.save()
                    return redirect('success')
        else:
            request.session['event_data'].update(request.POST.dict())

    else:
        initial_data = request.session.get('event_data', {})
        form = EventForm(initial=initial_data)

    context = {
        'form': form,
        'step': step,
    }
    return render(request, 'event/create.html', context)