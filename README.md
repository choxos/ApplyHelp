# ApplyHelp - Kurdish Students Study Abroad Platform

A comprehensive Django-based web platform designed to help Kurdish students from all regions (Rojhelat, Başûr, Bakûr, and Rojava) apply for MSc and PhD programs in Europe, Canada, USA, Australia, and New Zealand.

## 🌟 Features

### Core Functionality
- **Trilingual Support**: Kurdish Sorani (ckb), Kurdish Kurmanji (kmr), and English (en)
- **Destination Selection**: Smart matching system for countries and universities
- **Resume/CV Builder**: Professional templates adapted to different country standards
- **Communication Tools**: Email templates and application tracking
- **Comprehensive Resources**: Guides, success stories, and country-specific information

### Regional Support
The platform specifically addresses the unique challenges faced by Kurdish students from:
- **Rojhelat** (Eastern Kurdistan) - Different educational systems and documentation
- **Başûr** (Southern Kurdistan) - Semi-autonomous educational framework
- **Bakûr** (Northern Kurdistan) - Educational restrictions and language challenges
- **Rojava** (Western Kurdistan) - War-affected region with limited institutional access

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ApplyHelp.git
   cd ApplyHelp
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   Open your browser and go to `http://127.0.0.1:8000`

## 🏗️ Project Structure

```
ApplyHelp/
├── accounts/                 # User management and authentication
│   ├── models.py            # KurdishUser, UserProfile models
│   ├── views.py             # Authentication and profile views
│   ├── forms.py             # User registration and profile forms
│   └── urls.py              # Account-related URLs
├── destinations/            # Countries, universities, programs
│   ├── models.py            # Country, University, StudyProgram models
│   ├── views.py             # Destination browsing and comparison
│   └── urls.py              # Destination-related URLs
├── resume_builder/          # CV/Resume creation tools
│   ├── models.py            # Resume, Education, Experience models
│   ├── views.py             # Resume building interface
│   └── urls.py              # Resume builder URLs
├── communications/          # Email templates and application tracking
│   ├── models.py            # EmailTemplate, ApplicationTracker models
│   ├── views.py             # Communication tools and tracking
│   └── urls.py              # Communication URLs
├── resources/               # Guides, articles, success stories
│   ├── models.py            # Guide, Article, SuccessStory models
│   ├── views.py             # Resource browsing and display
│   └── urls.py              # Resource URLs
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── home.html            # Homepage
│   └── accounts/            # Account-specific templates
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── main.css         # Main styles
│   │   └── rtl.css          # Right-to-left styles for Kurdish
│   └── js/                  # JavaScript files
├── locale/                  # Translation files
├── media/                   # User-uploaded files
└── manage.py               # Django management script
```

## 🌐 Internationalization

The platform supports three languages with proper RTL (right-to-left) support for Kurdish:

- **Kurdish Sorani (ckb)**: Primary language, main interface
- **Kurdish Kurmanji (kmr)**: Northern Kurdish dialect support
- **English (en)**: International accessibility

### Adding Translations

1. **Create translation files**
   ```bash
   python manage.py makemessages -l ckb
   python manage.py makemessages -l kmr
   ```

2. **Compile translations**
   ```bash
   python manage.py compilemessages
   ```

## 📱 Key Models

### User Management
- **KurdishUser**: Extended user model with regional and academic information
- **UserProfile**: Detailed profile with biography, skills, and documents
- **KurdishDialect**: Language dialect tracking

### Destinations
- **Country**: Destination countries with study information
- **University**: Comprehensive university database
- **StudyProgram**: Specific programs and requirements
- **Scholarship**: Funding opportunities

### Resume Builder
- **Resume**: User resumes with multiple templates
- **Education**: Academic background entries
- **Experience**: Work and research experience
- **Skill**: Technical and language skills
- **Publication**: Research publications
- **Award**: Academic and professional achievements

### Communications
- **EmailTemplate**: Professional email templates
- **ApplicationTracker**: Application status tracking
- **EmailLog**: Communication history
- **CommunicationTip**: Cultural guidance and tips

### Resources
- **Guide**: Step-by-step guides and tutorials
- **ResourceCategory**: Organized resource categories
- **FAQ**: Frequently asked questions

## 🎨 Design Features

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Kurdish Typography**: Proper font support for Kurdish scripts
- **RTL Support**: Complete right-to-left layout for Kurdish languages
- **Regional Colors**: Color schemes representing Kurdish regions
- **Accessible**: WCAG compliant with keyboard navigation support

## 🔧 Development

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
For production, update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'applyhelp_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Running Tests
```bash
python manage.py test
```

### Translation Management
Use Django Rosetta for web-based translation management:
```bash
# Visit /rosetta/ after starting the server
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend
5. Set up SSL certificate
6. Configure domain and allowed hosts

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "kurdish_apply.wsgi:application"]
```

## 🤝 Contributing

We welcome contributions from the Kurdish community and supporters worldwide!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Translation Contributions
- Help translate the interface into Kurdish dialects
- Review and improve existing translations
- Add regional-specific content

### Content Contributions
- Add university and program information
- Write guides for specific countries or processes
- Share success stories
- Contribute email templates

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For community questions and ideas
- **Email**: support@applyhelp.org (when available)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Kurdish students and community members who provided feedback
- Open source contributors and maintainers
- Educational institutions supporting Kurdish students
- Translation volunteers and content creators

---

**Made with ❤️ for Kurdish students worldwide**

*"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela*