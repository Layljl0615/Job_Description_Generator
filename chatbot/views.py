from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from openai import OpenAI
from .models import Past, UserProfile
from .forms import ProfileUpdateForm, PasswordChangeWithSecurityForm
from django.core.paginator import Paginator
import os 

# Create OpenAI client once, using the env var loaded by manage.py
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # Fail fast so you see a clear error in the server logs instead of a 401 later
    raise RuntimeError("OPENAI_API_KEY is not set. Ensure .env is next to manage.py and is loaded.")
client = OpenAI(api_key=API_KEY)


def build_jd_prompt(job_title, tech_skills, experience_level, location, optional_notes):
    """
    Combine 4 required fields plus 1 optional free-text field into a clear prompt.
    """
    base_prompt = f"""
You are an experienced technical recruiter and HR specialist.

Based on the following information, write a complete job description in English.

- Job Title: {job_title}
- Tech Skills: {tech_skills}
- Experience Level: {experience_level}
- Location: {location}
"""

    if optional_notes:
        base_prompt += f"- Extra notes from the user (optional): {optional_notes}\n"

    base_prompt += """
Requirements:

* Start with the job title as a heading.
* Then add a section "Responsibilities:" as bullet points.
* Then a section "Requirements:" as bullet points.
* Optionally add a "Nice to Have:" section if it makes sense.
* End with a short paragraph about location / remote policy and company culture.
* Length around 300 to 500 words.
"""
    return base_prompt


# Create Homepage
@login_required(login_url='login')
def home(request):
    default_context = {
        "job_title": "",
        "tech_skills": "",
        "experience_level": "",
        "location": "",
        "company_tone": "",
        "job_description": "",
    }
    saved_context = request.session.get("last_generation")
    context = default_context.copy()

    if saved_context:
        context.update(saved_context)

    if request.method == "POST":
        job_title = request.POST.get("job_title", "").strip()
        tech_skills = request.POST.get("tech_skills", "").strip()
        experience_level = request.POST.get("experience_level", "").strip()
        location = request.POST.get("location", "").strip()
        optional_notes = request.POST.get("company_tone", "").strip()

        company_tone = optional_notes
        job_description = ""

        context.update(
            {
                "job_title": job_title,
                "tech_skills": tech_skills,
                "experience_level": experience_level,
                "location": location,
                "company_tone": optional_notes,
            }
        )

        user_prompt = build_jd_prompt(
            job_title,
            tech_skills,
            experience_level,
            location,
            optional_notes,
        )

        try:
            # call OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You write polished, professional job descriptions.",
                    },
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=700,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            job_description = response.choices[0].message.content.strip()

            if not job_description:
                job_description = "No response received from the model."

            lines = [
                f"Job Title: {job_title}",
                f"Tech Skills: {tech_skills}",
                f"Experience Level: {experience_level}",
                f"Location: {location}",
            ]

            if optional_notes:
                lines.append(f"Optional: {optional_notes}")

            question_for_history = "\n".join(lines)

            Past.objects.create(
                question=question_for_history,
                answer=job_description,
                user=request.user,
            )

            context["job_description"] = job_description

        except Exception as e:
            context["job_description"] = f"Error generating job description: {e}"

        request.session["last_generation"] = {
            "job_title": job_title,
            "tech_skills": tech_skills,
            "experience_level": experience_level,
            "location": location,
            "company_tone": company_tone,
            "job_description": context.get("job_description", ""),
        }

    return render(request, 'home.html', context)


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
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')

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
            # Check if security question and answer are provided
            elif not security_question or not security_answer:
                messages.error(request, "Please provide security question and answer!")
                return redirect('register')
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                # Create user profile with security question
                UserProfile.objects.create(
                    user=user,
                    security_question=security_question,
                    security_answer=security_answer
                )
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

    # Get security questions for the form
    security_questions = UserProfile.SECURITY_QUESTIONS
    return render(request, 'register.html', {'security_questions': security_questions})


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
            # Save identity to avoid re-entry --- IGNORE ---
            return render(request, 'login.html', {'username': username})

    return render(request, 'login.html', {})


# User Logout View
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')


# Edit Profile View
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('edit_profile')
                
        elif form_type == 'password':
            password_form = PasswordChangeWithSecurityForm(request.user, request.POST)
            if password_form.is_valid():
                # Change password
                new_password = password_form.cleaned_data['new_password1']
                request.user.set_password(new_password)
                request.user.save()
                # Keep user logged in after password change
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
                return redirect('edit_profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeWithSecurityForm(user=request.user)
    
    # Get user's security question for display
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        security_question_text = dict(UserProfile.SECURITY_QUESTIONS)[user_profile.security_question]
    except UserProfile.DoesNotExist:
        security_question_text = "Not set"
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'security_question_text': security_question_text
    }
    
    return render(request, 'edit_profile.html', context)
