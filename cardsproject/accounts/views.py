# from django.shortcuts import render
# from django.contrib.auth.models import User
# from django.urls import reverse_lazy
# from django.views.generic import CreateView

# from .forms import SignupForm
# # Create your views here.

# class SignupView(CreateView):
#     model = User
#     form_class = SignupForm
#     template_name = 'accounts/signup.html'
#     accounts_url = reverse_lazy('index')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
