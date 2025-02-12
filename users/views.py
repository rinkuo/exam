from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView, View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import UserProfileForm
from .models import UserProfile


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully! 🎉")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your sign-up. 🚨")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class UserLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        
        if user:
            login(self.request, user)
            messages.success(self.request, "Logged in successfully! 🚀")
            return redirect(self.get_success_url())

        messages.error(self.request, "Invalid email or password. ❌ suck my dick")
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully! ✅")
        return reverse_lazy('users:profile')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        # Ensure you're updating the profile, not the CustomUser
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form if needed
        return kwargs

    def form_valid(self, form):
        # Check if we are removing the image
        if form.cleaned_data.get('clear_image'):
            self.request.user.profile.image = None  # Clear the profile image

        # Now handle saving the form (image upload)
        form.save()

        # Handle password change if applicable
        new_password = form.cleaned_data.get("new_password")
        if new_password:
            self.request.user.set_password(new_password)
            self.request.user.save()

        messages.success(self.request, "Profile updated successfully! 🎉")
        return redirect('users:profile')

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your update. ❌")
        return self.render_to_response({'form': form})



class CustomLogoutView(View):
    def get(self, request):
        return render(request, 'users/confirm_logout.html')

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out. 👋")
        return redirect('users:success_logout')


class SuccessLogoutView(View):
    def get(self, request):
        return render(request, 'users/success_logout.html')
