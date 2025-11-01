from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from openai import OpenAI
from .models import Past
from django.core.paginator import Paginator
import os  # ✅ added

# Create OpenAI client once, using the env var loaded by manage.py
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # Fail fast so you see a clear error in the server logs instead of a 401 later
    raise RuntimeError("OPENAI_API_KEY is not set. Ensure .env is next to manage.py and is loaded.")
client = OpenAI(api_key=API_KEY)

# Create Homepage
@login_required(login_url='login')
def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']

        try:
            # Make a Completion using new API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": question}
                ],
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # Parse the response
            answer = response.choices[0].message.content.strip()

            # Check if we got a valid answer
            if not answer:
                answer = "No response received from ChatGPT."

            # Logic for Past responses
            if "41elder41" in past_responses:
                past_responses = answer
            else:
                past_responses = f"{past_responses}<br/><br/>{answer}"

            # Save To Database
            record = Past(question=question, answer=answer, user=request.user)
            record.save()

            return render(request, 'home.html', {"question": question, "response": answer, "past_responses": past_responses})

        except Exception as e:
            # If there's an error, don't show the 41elder41 marker
            if "41elder41" in past_responses:
                past_responses = ""
            error_message = f"Error: {str(e)}"
            print(f"API Error: {error_message}")  # Log to console
            return render(request, 'home.html', {"question": question, "response": error_message, "past_responses": error_message})

    return render(request, 'home.html', {})


@login_required(login_url='login')
def past(request):
    # Set up pagination for current user's records only
    p = Paginator(Past.objects.filter(user=request.user), 5)
    page = request.GET.get('page')
    pages = p.get_page(page)

    # Queried The Database - only current user's records
    past = Past.objects.filter(user=request.user)

    # Get number of pages
    nums = "a" * pages.paginator.num_pages

    return render(request, 'past.html', {"past": past, "pages": pages, "nums": nums})


@login_required(login_url='login')
def delete_past(request, Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, ("That Question and Answer have been deleted..."))
    return redirect('past')


# User Registration View
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 == password2:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('register')
            # Check if email already exists
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('register')
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

    return render(request, 'register.html', {})


# User Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html', {})


# User Logout View
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')
