# SkillSwap 🔄

> **Trade Skills, Not Money** - A community-driven platform for exchanging skills using a time-based credit system.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 About

SkillSwap is a web application that enables people to exchange skills without money. Whether you want to learn photography, get coding help, or master a language, you can trade your own skills to learn from others.

### Key Features

- 🎓 **Skill Marketplace** - Browse and offer skills across multiple categories
- ⏱️ **Time Credit System** - Use time-based credits instead of money
- 🔄 **Exchange Management** - Propose, accept, and complete skill exchanges
- ⭐ **Review System** - Rate and review your exchange partners
- 💬 **Direct Messaging** - Communicate with other users
- 👥 **Communities** - Join local skill-sharing groups
- 📊 **Dashboard** - Track your exchanges, credits, and stats

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Sample Data](#sample-data)
- [Project Structure](#project-structure)
- [Features Overview](#features-overview)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** (recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/skillswap.git
cd skillswap_project
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/development.txt
```

### 4. Environment Setup

Create a `.env` file in the project root:

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_NAME=db.sqlite3

# Email (Console backend for development)
DEFAULT_FROM_EMAIL=noreply@skillswap.local
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Load Sample Data

```bash
python manage.py create_sample_data
```

This creates 6 test users, skill offers, exchanges, and more!

## ▶️ Running the Application

### Development Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

### Access Points

- **Home**: http://localhost:8000
- **Browse Skills**: http://localhost:8000/skills/browse/
- **How It Works**: http://localhost:8000/how-it-works/
- **Login**: http://localhost:8000/accounts/login/
- **Admin Panel**: http://localhost:8000/admin/

## 👥 Sample Data

After running `create_sample_data`, you can login with these test accounts:

| Username | Password | Role |
|----------|----------|------|
| alice_dev | password123 | Developer |
| bob_chef | password123 | Chef |
| carol_artist | password123 | Artist |
| david_musician | password123 | Musician |
| emma_linguist | password123 | Language Teacher |
| frank_fitness | password123 | Fitness Trainer |

All users start with **5 credits**, and some have bonus credits!

## 📁 Project Structure

```
skillswap_project/
├── apps/
│   ├── accounts/          # User authentication & profiles
│   ├── skills/            # Skill offers & requests
│   ├── exchanges/         # Exchange management
│   ├── credits/           # Time credit system
│   ├── reviews/           # Rating & review system
│   ├── messaging/         # Direct messaging
│   ├── communities/       # Community hubs
│   └── core/              # Shared utilities
├── config/
│   ├── settings/          # Split settings (base, dev, prod)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
├── media/                 # User uploads
├── requirements/          # Dependency files
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
└── README.md              # This file
```

## ✨ Features Overview

### 1. User Management
- Registration and authentication
- User profiles with bios and stats
- Credit balance tracking
- Exchange history

### 2. Skill Marketplace
- Browse skills by category
- Filter by delivery method (in-person/video call)
- Search functionality
- Detailed skill pages with teacher info

### 3. Exchange System
- Propose skill exchanges
- Accept/decline requests
- Confirm completion (both parties)
- Automatic credit transfer

### 4. Credit System
- Time-based credits (1 credit = 1 hour)
- Starting balance: 5 credits
- Earn credits by teaching
- Spend credits to learn
- Transaction history

### 5. Reviews & Ratings
- 5-star rating system
- Skill quality assessment
- Communication & reliability ratings
- Public reviews on profiles

### 6. Communities
- Join local skill-sharing groups
- View community members
- Community-specific exchanges

### 7. Messaging
- Direct messaging between users
- Conversation threads
- Message notifications

## 🛠️ Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 guidelines. Use `flake8` for linting:

```bash
pip install flake8
flake8 apps/
```

### Database Migrations

After model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Clearing Sample Data

To start fresh:

```bash
python manage.py flush
python manage.py create_sample_data
```

## 🔒 Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False`
3. Update `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Configure proper email backend
6. Enable HTTPS
7. Set up static file serving (whitenoise/nginx)

## 🎨 Tech Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, Tailwind CSS, HTMX
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Authentication**: Django Auth
- **File Storage**: Local (dev), S3-compatible (prod)

## 📦 Dependencies

### Core
- Django 4.2+
- Pillow (image processing)
- python-decouple (environment variables)

### Development
- django-debug-toolbar
- ipython

### Production
- psycopg2-binary (PostgreSQL)
- gunicorn (WSGI server)
- whitenoise (static files)

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Known Issues

- None currently! Report bugs via [GitHub Issues](https://github.com/yourusername/skillswap/issues)

## 📝 To-Do

- [ ] Email notifications
- [ ] Calendar integration for scheduling
- [ ] Mobile app
- [ ] Payment gateway for credit purchases
- [ ] Advanced search filters
- [ ] Skill badges and achievements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django community for excellent documentation
- Tailwind CSS for beautiful styling
- All beta testers and contributors

## 📞 Support

For support:
- 📧 Email: support@skillswap.local
- 💬 Discord: [Join our server](https://discord.gg/skillswap)
- 📖 Docs: [Read the docs](https://docs.skillswap.local)

---

**Made with ❤️ by the SkillSwap Team**

⭐ **Star this repo if you find it useful!**
