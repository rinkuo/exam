from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from pyexpat.errors import messages

from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'})
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'})
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'})
    )

    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-md'})
    )

    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        label="New Password"
    )

    repeat_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        label="Repeat Password"
    )

    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'bio', 'location', 'birth_date', 'image', 'new_password']

        new_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Access the related UserProfile to get first_name and last_name
            user_profile = user.profile
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user_profile.first_name
            self.fields['last_name'].initial = user_profile.last_name

        for field_name in self.fields:
            if field_name not in ["birth_date", "new_password", "repeat_password"]:
                self.fields[field_name].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border rounded-md'
                })

        self.fields['bio'].widget.attrs.update({'rows': '4'})

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        clear_image = cleaned_data.get('clear_image')

        # Ensure that only one of the image field or clear checkbox is selected
        if image and clear_image:
            raise forms.ValidationError("Please either submit a file or check the clear checkbox, not both.")

        return cleaned_data
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user_profile.user.set_password(new_password)
            user_profile.user.save()

        user_profile.user.username = self.cleaned_data.get("username")
        user_profile.user.email = self.cleaned_data.get("email")
        user_profile.user.save()


        user_profile.first_name = self.cleaned_data.get("first_name")
        user_profile.last_name = self.cleaned_data.get("last_name")
        user_profile.phone_number = self.cleaned_data.get("phone_number")
        user_profile.bio = self.cleaned_data.get("bio")
        user_profile.location = self.cleaned_data.get("location")
        user_profile.birth_date = self.cleaned_data.get("birth_date")

        if commit:
            user_profile.save()

        return user_profile


