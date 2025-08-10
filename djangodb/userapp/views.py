from django.shortcuts import render, redirect  # Used to render templates and redirect after login
from django.contrib.auth import authenticate, login ,logout # Used to check user credentials and log them in
from django.contrib import messages  # Used to display success/error messages to users
from .forms import LoginForm  # Now this will work
 # Import the custom login form we created

# This function handles the login process using a form model (LoginForm)
def user_login(request):
    # Check if the request method is POST (i.e., form submitted)
    if request.method == 'POST':
        # Bind form data to the LoginForm
        form = LoginForm(request.POST)
        

        # Validate the form inputs
        if form.is_valid():
            # Extract username and password from the cleaned form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user using Django's built-in authenticate function
            user = authenticate(request, username=username, password=password)

            # If user credentials are correct, log them in
            if user is not None:
                login(request, user)  # Logs the user in and starts a session
                messages.success(request, 'Login successful')  # Show success message
                return redirect('index')  # Redirect the user to homepage or desired page
            else:
                # If credentials are incorrect, show error message
                messages.error(request, 'Invalid username or password')
    else:
        # If the request method is GET, display an empty login form
        form = LoginForm()

    # Render the login page and pass the form to the template
    return render(request, 'userapp/login.html', {'form': form})


def user_logout(request):
    logout(request) # Log the user out
    messages.success(request, 'You have been logged out successfully')  # Show logout success message
    return redirect('index')