from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from allauth.account.forms import SignupForm

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
