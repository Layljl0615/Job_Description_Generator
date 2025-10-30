# Job Description Generator

An intelligent AI-powered application built with Django and OpenAI API for generating job descriptions through natural conversations, featuring user authentication and conversation history management.

## Features

- 🤖 **AI-Powered Chat**: Integrated with OpenAI GPT-3.5-turbo model for intelligent conversations
- 👤 **User Authentication**: Complete user registration, login, and logout functionality
- 📝 **Conversation History**: Save and view personal conversation records
- 🔒 **Privacy Protection**: Users can only view their own conversation history
- 🗑️ **Record Management**: Support for deleting conversation history

## Tech Stack

- **Backend Framework**: Django 4.2.25
- **Database**: SQLite3
- **AI Service**: OpenAI API (gpt-3.5-turbo)
- **Frontend**: Bootstrap 5 + Django Templates
- **Python Version**: Python 3.9+

## Requirements

- Python 3.9 or higher
- pip (Python package manager)
- OpenAI API Key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Layljl0615/Job_Description_Generator.git
cd Job_Description_Generator
```

### 2. Create Virtual Environment

```bash
python3.9 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install django==4.2.25
pip install openai==2.6.1
pip install python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **Important**: Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 5. Database Migration

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

After the server starts, visit http://127.0.0.1:8000/

## Usage

### Register an Account

1. Visit the homepage and click the "Register" button in the navigation bar
2. Fill in username, email, and password
3. After successful registration, you will be automatically logged in

### Start a Conversation

1. After logging in, enter your question in the input box on the homepage
2. Click the "Submit" button
3. AI will generate a response and display it on the page

### View History

1. Click the "Past Questions" button in the navigation bar
2. View all conversation history
3. Click "Delete" to remove unwanted records

## Project Structure

```
Job_Description_Generator/
├── chatbot/                 # Main application
│   ├── migrations/         # Database migration files
│   ├── templates/          # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── home.html      # Home page
│   │   ├── login.html     # Login page
│   │   ├── register.html  # Registration page
│   │   ├── past.html      # History page
│   │   └── navbar.html    # Navigation bar
│   ├── models.py          # Data models
│   ├── views.py           # View functions
│   └── urls.py            # URL routing
├── chatgpt/                # Project configuration
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
├── manage.py              # Django management script
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

## Data Models

### Past Model

Stores user conversation history:

- `user`: Foreign key to Django User model
- `prompt`: User's question
- `response`: AI's response
- `created_at`: Creation timestamp

## Security Notes

- ✅ API keys are managed through environment variables and not committed to Git
- ✅ Database file `db.sqlite3` is added to `.gitignore`
- ✅ User passwords are encrypted using Django's built-in security
- ✅ All conversation features require login access

## Development Notes

### Update views.py to Use Environment Variables

Ensure that the OpenAI client in `chatbot/views.py` reads the API key from environment variables:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

### Dependency Management

If you add new dependencies, it's recommended to create a `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Other developers can install all dependencies with:

```bash
pip install -r requirements.txt
```

## Troubleshooting

### Issue 1: OpenAI API Error

Make sure:
- `.env` file exists and contains a valid API key
- API key has sufficient quota
- Network connection is working

### Issue 2: Database Error

Run migration command:
```bash
python manage.py migrate
```

### Issue 3: Static Files Not Loading

Run the following command to collect static files:
```bash
python manage.py collectstatic
```

## Contributing

Issues and Pull Requests are welcome!

## License

This project is for learning and research purposes only.

## Contact

- GitHub: [@Layljl0615](https://github.com/Layljl0615)
- Repository: [Job_Description_Generator](https://github.com/Layljl0615/Job_Description_Generator)

---

⭐ If this project helps you, please give it a star!
