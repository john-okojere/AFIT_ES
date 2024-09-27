from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from allauth.account.forms import SignupForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from event.models import Event, Payment

@login_required
def user_profile(request):
    # Get the logged-in user's details
    user = request.user

    # Fetch events the user has purchased tickets for
    payments = Payment.objects.filter(ticket__event__category__name="Event").select_related('ticket', 'ticket__event')

    # Render the profile template with user details and past payments/events
    context = {
        'user': user,
        'payments': payments,
    }
    return render(request, 'user/profile.html', context)

def custom_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            # Authenticate the user
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')  # or however you handle passwords
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('/')  # Redirect to a logged-in page
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})
