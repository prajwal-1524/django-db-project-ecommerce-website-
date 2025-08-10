from django.shortcuts import render, redirect  # Used to render templates and redirect after login
from django.contrib.auth import authenticate, login ,logout # Used to check user credentials and log them in
from django.contrib import messages  # Used to display success/error messages to users
from .forms import LoginForm  # Now this will work
 # Import the custom login form we created
from .forms import UserSignUpForm, VendorSignUpForm  # Import the signup forms 

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

def signup(request):
    if request.method == 'POST': #
        user_form = UserSignUpForm(request.POST) #frontend ma we show usersignupform and data filled up are stored in user_form object
        vendor_form = VendorSignUpForm(request.POST, request.FILES) # Handle file uploads for vendor logo

    if user_form.is_valid():
    # Create user instance but don't save to database yet
    user = user_form.save(commit=False)
    
    # Get the 'is_vendor' value from the form (True if checked, False if not)
    user.is_vendor = user_form.cleaned_data.get('is_vendor')
    
    # Save the user instance to the database with the updated 'is_vendor' field
    user.save()
    
    if user.is_vendor:
        #user.is_vendor = True  # Set the user as a vendor if the checkbox is checked
        #user.is_vendor = user_form.cleaned_data['is_vendor']  # Get the value from the form
        #If the user is a vendor, save the vendor form data
        vendor = vendor_form.save(commit=False) #saves the form data to user model in database 
        vendor.user = user  #You’re linking the vendor object to the user object by setting the user field on the vendor model to point to this specific user.
        vendor.save()  # Save the vendor instance to the database

        login(request, user)  # Log the user in after successful signup
        messages.success(request, 'Signup successful! You are now logged in.')
        return redirect('index')  # Redirect to homepage or desired page

    else:
        messages.error(request, 'There was an error with your signup. Please try again.')

    else:
        user_form = UserSignUpForm() # Create an empty user signup form
        vendor_form = VendorSignUpForm() # Create an empty vendor signup form

    # Render the signup page and pass both forms to the template
    return render(request, 'userapp/signup.html', {'user_form': user_form, 'vendor_form': vendor_form})   