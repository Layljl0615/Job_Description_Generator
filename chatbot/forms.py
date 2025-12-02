from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    # Common email domains in the US and China
    VALID_EMAIL_DOMAINS = [
        # Common US email domains
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
        'aol.com', 'icloud.com', 'mail.com', 'msn.com',
        'live.com', 'comcast.net', 'att.net', 'verizon.net',
        'sbcglobal.net', 'cox.net', 'earthlink.net', 'juno.com',
        'ymail.com', 'rocketmail.com', 'me.com', 'mac.com',
        
        # Common Chinese email domains
        'qq.com', '163.com', '126.com', 'sina.com', 'sina.cn',
        'sohu.com', 'aliyun.com', 'hotmail.com.cn', 'outlook.com.cn',
        'foxmail.com', 'gmail.com.cn'
    ]
    
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
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        """
        Validate that the email domain is in our list of valid domains
        """
        email = self.cleaned_data.get('email')
        if email:
            try:
                domain = email.split('@')[1].lower()
                if domain not in self.VALID_EMAIL_DOMAINS:
                    raise ValidationError(
                        f'Email domain "{domain}" is not allowed. Please use a common email provider.'
                    )
            except IndexError:
                raise ValidationError('Invalid email format.')
        return email

    def save(self, commit=True):
        """
        Save the user and create their profile with security question
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        security_question = self.cleaned_data["security_question"]
        security_answer = self.cleaned_data["security_answer"]
        if commit:
            user.save()
            # Create user profile with security question
            UserProfile.objects.create(
                user=user,
                security_question=security_question,
                security_answer=security_answer
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    # Common email domains in the US and China
    VALID_EMAIL_DOMAINS = [
        # Common US email domains
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
        'aol.com', 'icloud.com', 'mail.com', 'msn.com',
        'live.com', 'comcast.net', 'att.net', 'verizon.net',
        'sbcglobal.net', 'cox.net', 'earthlink.net', 'juno.com',
        'ymail.com', 'rocketmail.com', 'me.com', 'mac.com',
        
        # Common Chinese email domains
        'qq.com', '163.com', '126.com', 'sina.com', 'sina.cn',
        'sohu.com', 'aliyun.com', 'hotmail.com.cn', 'outlook.com.cn',
        'foxmail.com', 'gmail.com.cn'
    ]
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_email(self):
        """
        Validate that the email domain is in our list of valid domains
        """
        email = self.cleaned_data.get('email')
        if email:
            try:
                domain = email.split('@')[1].lower()
                if domain not in self.VALID_EMAIL_DOMAINS:
                    raise ValidationError(
                        f'Email domain "{domain}" is not allowed. Please use a common email provider.'
                    )
            except IndexError:
                raise ValidationError('Invalid email format.')
        return email


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
        """
        Validate the security question answer
        """
        answer = self.cleaned_data.get('security_answer')
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            if answer.lower() != user_profile.security_answer.lower():
                raise forms.ValidationError("Incorrect security answer")
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("User profile not found")
        return answer
    
    def clean_new_password2(self):
        """
        Validate that the two password fields match
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2