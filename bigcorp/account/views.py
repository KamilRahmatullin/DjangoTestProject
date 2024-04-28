from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import UserCreateForm
from django_email_verification import send_email

User = get_user_model()


# Register user view
def register_user_view(request):
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
