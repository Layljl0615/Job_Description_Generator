from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Past
from unittest.mock import patch, MagicMock


class PastModelTest(TestCase):
    def setUp(self):
        """Set up test data for the model tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.past_entry = Past.objects.create(
            user=self.user,
            question='Test job title: Software Engineer',
            answer='This is a test job description.'
        )

    def test_past_model_str(self):
        """Test the string representation of the Past model."""
        self.assertEqual(str(self.past_entry), 'Test job title: Software Engineer')

    def test_past_model_fields(self):
        """Test the fields of the Past model."""
        past = Past.objects.get(id=self.past_entry.id)
        self.assertEqual(past.user.username, 'testuser')
        self.assertEqual(past.question, 'Test job title: Software Engineer')
        self.assertEqual(past.answer, 'This is a test job description.')

    def test_past_model_ordering(self):
        """Test that Past model orders by created_at descending."""
        # Create another entry to test ordering
        past2 = Past.objects.create(
            user=self.user,
            question='Second job title',
            answer='Second job description.'
        )

        past_entries = Past.objects.all()
        # The most recent entry should be first
        self.assertEqual(past_entries.first(), past2)


class ViewsTest(TestCase):
    def setUp(self):
        """Set up test data for the view tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_home_view_get(self):
        """Test the home view renders correctly for GET requests."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view_get(self):
        """Test the register view renders correctly for GET requests."""
        self.client.logout()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view_get(self):
        """Test the login view renders correctly for GET requests."""
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_past_view_get(self):
        """Test the past view renders correctly for GET requests."""
        response = self.client.get(reverse('past'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'past.html')

    @patch('chatbot.views.client.chat.completions.create')
    def test_home_view_post_success(self, mock_create):
        """Test the home view handles POST requests successfully."""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test job description from AI"
        mock_create.return_value = mock_response

        form_data = {
            'job_title': 'Software Engineer',
            'tech_skills': 'Python, Django, JavaScript',
            'experience_level': 'Mid-level',
            'location': 'Remote',
            'company_tone': 'Friendly'
        }

        response = self.client.post(reverse('home'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        # Check that a Past entry was created
        self.assertTrue(Past.objects.filter(question__icontains='Software Engineer').exists())

        # Check that the mock was called with correct parameters
        mock_create.assert_called_once()



    def test_register_user_password_mismatch(self):
        """Test user registration with mismatched passwords."""
        self.client.logout()
        form_data = {
            'username': 'newuser',
            'email': 'newuser@icloud.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword',
            'security_question': 'favorite_color',
            'security_answer': 'blue'
        }
    
        response = self.client.post(reverse('register'), form_data)
        # Password mismatch should stay on register page with error (status code 200)
        self.assertEqual(response.status_code, 200)
    
        # Check that the user was not created
        self.assertFalse(User.objects.filter(username='newuser').exists())


    def test_login_user_success(self):
        """Test successful user login."""
        self.client.logout()
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        response = self.client.post(reverse('login'), form_data)
        self.assertRedirects(response, reverse('home'))

    def test_logout_user(self):
        """Test user logout."""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_register_user_invalid_email_domain(self):
        """Test user registration fails with invalid email domain."""
        self.client.logout()
        form_data = {
            'username': 'newuser',
            'email': 'newuser@invalid-domain.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'security_question': 'favorite_color',
            'security_answer': 'blue'
        }
        
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on register page with error
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_edit_profile_invalid_email_domain(self):
        """Test profile update fails with invalid email domain."""
        form_data = {
            'form_type': 'profile',
            'username': 'testuser',
            'email': 'testuser@invalid-domain.com'
        }
        
        response = self.client.post(reverse('edit_profile'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on edit profile page with error
        # Check that the user's email was not changed
        user = User.objects.get(username='testuser')
        self.assertNotEqual(user.email, 'testuser@invalid-domain.com')

    def test_edit_profile_valid_email_domain(self):
        """Test successful profile update with valid email domain."""
        form_data = {
            'form_type': 'profile',
            'username': 'testuser',
            'email': 'testuser@gmail.com'
        }
        
        response = self.client.post(reverse('edit_profile'), form_data)
        self.assertRedirects(response, reverse('edit_profile'))
        # Check that the user's email was changed
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@gmail.com')
