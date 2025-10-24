from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        # Process the completed form.
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and redirect to the home page.
            login(request, new_user)
            return redirect('/')
    else:
        # Display a blank registration form.
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)