from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    security_question = forms.ChoiceField(
        choices=UserProfile.SECURITY_QUESTIONS,
        label="Security Question",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    security_answer = forms.CharField(
        max_length=100,
        label="Security Answer",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "security_question", "security_answer")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Create user profile with security question
            UserProfile.objects.create(
                user=user,
                security_question=self.cleaned_data["security_question"],
                security_answer=self.cleaned_data["security_answer"]
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordChangeWithSecurityForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Current Password'
    )
    security_answer = forms.CharField(
        max_length=100,
        label='Security Question Answer',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm New Password'
    )
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_security_answer(self):
        answer = self.cleaned_data.get('security_answer')
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            if answer.lower() != user_profile.security_answer.lower():
                raise forms.ValidationError("Incorrect security answer")
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("User profile not found")
        return answer
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2