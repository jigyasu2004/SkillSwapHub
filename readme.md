# Skill Swap Platform

## Overview

The Skill Swap Platform is a web-based application that enables users to exchange skills with one another. Built with Flask and SQLAlchemy, it provides a comprehensive platform for users to list their offered skills, specify wanted skills, and arrange skill exchanges with other platform members.

## Local Setup Guide

This guide will help you set up and run the Skill Swap Platform on your local Windows PC.

### Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **PostgreSQL Database** - You can use:
   - Local PostgreSQL installation
   - Cloud database (Neon, Supabase, etc.)
   - PostgreSQL Docker container

### Setup Instructions

#### 1. Download the Project

Clone or download the project files to your computer:
```bash
git clone https://github.com/jigyasu2004/SkillSwapHub.git
cd SkillSwapHub
```

#### 2. Create Virtual Environment

Open Command Prompt or PowerShell in the project directory:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# For Git Bash or WSL, use:
# source venv/Scripts/activate
```

#### 3. Install Dependencies

Install all required packages:
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file with your database details:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/skillswap_db
   SESSION_SECRET=your-super-secret-session-key-here
   ```

   **For cloud databases:**
   ```
   DATABASE_URL=postgresql://username:password@hostname:port/database_name
   ```

#### 5. Database Setup

If using local PostgreSQL:
1. Create a new database named `skillswap_db`
2. Update the `.env` file with your database credentials

The application will automatically create all required tables when you first run it.

#### 6. Run the Application

Start the development server:
```bash
# Make sure virtual environment is activated
python main.py
```

Or use Flask's development server:
```bash
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
```

The application will be available at: `http://localhost:5000`

### Production Deployment

For production deployment, use Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Database Configuration Examples

#### Local PostgreSQL
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/skillswap_db
```

#### Neon Database (Cloud)
```
DATABASE_URL=postgresql://username:password@ep-example-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

#### Supabase Database (Cloud)
```
DATABASE_URL=postgresql://postgres:password@db.example.supabase.co:5432/postgres
```

### Troubleshooting

#### Common Issues:

1. **Module not found errors**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt` again

2. **Database connection errors**
   - Check your `.env` file configuration
   - Ensure PostgreSQL is running
   - Verify database credentials

3. **Permission errors on Windows**
   - Run Command Prompt as Administrator
   - Use PowerShell instead of Command Prompt

4. **Port already in use**
   - Change the port: `flask run --port 8000`
   - Or kill the process using port 5000

#### Environment Variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for session encryption (generate a random string)
- `FLASK_ENV`: Set to `development` for debugging
- `FLASK_DEBUG`: Set to `1` for debug mode

### Features

- User registration and authentication
- Profile management with skills
- Skill swap request system
- Real-time messaging for accepted swaps
- User rating and feedback system
- Admin dashboard for moderation
- Responsive design for mobile and desktop

### Default Admin Account

The application creates sample data including an admin account:
- Username: `admin`
- Password: `admin123`

**Change this password immediately in production!**

### Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Check that PostgreSQL is running and accessible

### File Structure

```
skill-swap-platform/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── utils.py            # Utility functions
├── .env                # Environment variables (create this)
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── readme.md           # This file
```

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Session-based authentication with password hashing (Werkzeug)
- **Template Engine**: Jinja2 for server-side rendering
- **Deployment**: WSGI application with ProxyFix middleware

### Frontend Architecture
- **UI Framework**: Bootstrap 5.1.3 for responsive design
- **Icons**: Font Awesome 6.0.0
- **JavaScript**: Vanilla JavaScript with Bootstrap components
- **Styling**: Custom CSS with CSS variables for theming

### Database Design
- **ORM**: SQLAlchemy with declarative base
- **Connection Pooling**: Configured with pool recycling and pre-ping
- **Schema**: Relational design with proper foreign key relationships

## Key Components

### User Management
- User registration and authentication system
- Profile management (public/private visibility)
- Admin role with elevated permissions
- User banning and moderation capabilities

### Skill System
- Skill categories and classification
- User skill offerings and requests
- Skill-based search and filtering
- Dynamic skill assignment to users

### Swap Request System
- Request creation and management
- Accept/reject functionality
- Status tracking (pending, accepted, rejected, completed)
- Request deletion for pending requests

### Rating and Feedback
- Post-swap rating system
- Average rating calculation
- Feedback collection and display
- User reputation building

### Admin Dashboard
- User management and moderation
- Swap monitoring and statistics
- Platform-wide messaging system
- Activity reporting and analytics

### Search and Discovery
- Multi-criteria search (name, location, skills)
- Availability filtering
- Pagination for large result sets
- Real-time search suggestions

## Data Flow

### User Registration Flow
1. User submits registration form
2. Password validation and hashing
3. User account creation in database
4. Automatic login and session creation

### Skill Exchange Flow
1. User browses available skill providers
2. Sends swap request with offer details
3. Recipient receives notification
4. Request acceptance/rejection
5. Skill exchange coordination
6. Post-exchange rating and feedback

### Admin Moderation Flow
1. Admin monitors user activities
2. Reviews inappropriate content
3. Takes moderation actions (warnings, bans)
4. Sends platform notifications
5. Generates activity reports

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.1.3**: UI framework and responsive design
- **Font Awesome 6.0.0**: Icon library
- **Custom CSS**: Enhanced styling and animations

### Backend Libraries
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Werkzeug**: Password hashing and utilities
- **psycopg2**: PostgreSQL database adapter
- **python-dotenv**: Environment variable management
- **gunicorn**: WSGI server for production

### Database Service
- **PostgreSQL**: Database system (local or cloud)
- **SSL connection**: Secure database connectivity
- **Connection pooling**: Performance optimization

## Deployment Strategy

### Development Environment
- **Local Development**: Flask development server with python-dotenv
- **Hot Reload**: Debug mode enabled
- **Environment Variables**: .env file configuration management
- **Virtual Environment**: Isolated Python dependencies

### Local Setup Files
- **.env.example**: Template for environment variables
- **local_requirements.txt**: Python dependencies for local development
- **LOCAL_SETUP.md**: Complete setup guide for Windows/local development

### Database Configuration
- **Connection String**: Environment-based configuration via .env file
- **SSL Mode**: Required for secure connections (cloud databases)
- **Pool Settings**: Optimized for performance
- **Automatic Migration**: Table creation on startup
- **Multiple Database Support**: Local PostgreSQL or cloud providers (Neon, Supabase)

### Static Assets
- **CSS/JS Files**: Served via Flask static file handling
- **CDN Resources**: External libraries loaded from CDN
- **Asset Organization**: Structured static file directory

### Security Considerations
- **Password Hashing**: Werkzeug secure password storage
- **Session Management**: Flask session handling
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM protection

### Performance Optimizations
- **Database Pooling**: Connection reuse and management
- **Lazy Loading**: Efficient relationship loading
- **Pagination**: Large dataset handling
- **Caching Strategy**: Session-based state management

The application follows a traditional MVC pattern with clear separation of concerns, making it maintainable and scalable. The modular design allows for easy feature additions and modifications while maintaining code quality and performance standards.

## Performance Improvements

- **Caching**: Frequently used data (like the list of all skills) is cached in memory to reduce database load and speed up autocomplete and form rendering.
- **Debug Mode Disabled**: The application runs with `debug=False` in production for better performance and security.
- **Database Pooling**: Connection reuse and management is enabled for faster database access.
- **Pagination and Query Limits**: All large queries use pagination or limits to avoid loading too much data at once.
- **Frontend Optimizations**: Debouncing, lazy loading of images, and efficient DOM updates are used for a fast user experience.
- **Production WSGI Server**: Use Gunicorn or another WSGI server for production deployment instead of Flask's built-in server.