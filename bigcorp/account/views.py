from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_email_verification import send_email

from .forms import UserCreateForm, LoginForm, ProfileForm

User = get_user_model()


# Register user view
def register_user_view(request):
    """
    View function for registering a new user.

    This function handles the registration of a new user. If the request method is POST, it processes the form data,
    creates a new user, sends an email for verification, and redirects to the 'account:email_verification'
    page upon successful registration. If the request method is not POST,
    it renders the 'account/registration/register.html' template with the user registration form.
    """
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            # Create new user
            user = User.objects.create_user(
                username=user_username,
                email=user_email,
                password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('account:email_verification')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def login_user_view(request):
    """
    Display the login form and authenticate user credentials.
    """
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('shop:products')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('shop:products')
        return redirect('account:login')

    context = {
        'form': form
    }
    return render(request, 'account/login/login.html', context)


def logout_user_view(request):
    logout(request)
    return redirect('shop:products')


@login_required(login_url='account:login')
def dashboard_view(request):
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def profile_view(request):
    """
    View function for managing user profile.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'form': form
    }

    return render(request, 'account/dashboard/profile_management.html', context=context)


@login_required(login_url='account:login')
def delete_users_view(request):
    """
    View function for deleting the user account.

    This view function allows a logged-in user to delete their account. If the request method is POST, it deletes the user account
    and redirects to the 'shop:products' page. If the request method is not POST, it renders the 'account/dashboard/account_delete.html' template.
    """
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request, 'account/dashboard/account_delete.html')