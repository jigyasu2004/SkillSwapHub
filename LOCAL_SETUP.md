# Skill Swap Platform - Local Setup Guide

This guide will help you set up and run the Skill Swap Platform on your local Windows PC.

## Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **PostgreSQL Database** - You can use:
   - Local PostgreSQL installation
   - Cloud database (Neon, Supabase, etc.)
   - PostgreSQL Docker container

## Setup Instructions

### 1. Download the Project

Clone or download the project files to your computer:
```bash
git clone <repository-url>
cd skill-swap-platform
```

### 2. Create Virtual Environment

Open Command Prompt or PowerShell in the project directory:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# For Git Bash or WSL, use:
# source venv/Scripts/activate
```

### 3. Install Dependencies

Install all required packages:
```bash
pip install -r local_requirements.txt
```

### 4. Environment Configuration

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

### 5. Database Setup

If using local PostgreSQL:
1. Create a new database named `skillswap_db`
2. Update the `.env` file with your database credentials

The application will automatically create all required tables when you first run it.

### 6. Run the Application

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

## Production Deployment

For production deployment, use Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

## Database Configuration Examples

### Local PostgreSQL
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/skillswap_db
```

### Neon Database (Cloud)
```
DATABASE_URL=postgresql://username:password@ep-example-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Supabase Database (Cloud)
```
DATABASE_URL=postgresql://postgres:password@db.example.supabase.co:5432/postgres
```

## Troubleshooting

### Common Issues:

1. **Module not found errors**
   - Make sure virtual environment is activated
   - Run `pip install -r local_requirements.txt` again

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

### Environment Variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for session encryption (generate a random string)
- `FLASK_ENV`: Set to `development` for debugging
- `FLASK_DEBUG`: Set to `1` for debug mode

## Features

- User registration and authentication
- Profile management with skills
- Skill swap request system
- Real-time messaging for accepted swaps
- User rating and feedback system
- Admin dashboard for moderation
- Responsive design for mobile and desktop

## Default Admin Account

The application creates sample data including an admin account:
- Username: `admin`
- Password: `admin123`

**Change this password immediately in production!**

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Check that PostgreSQL is running and accessible

## File Structure

```
skill-swap-platform/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── utils.py            # Utility functions
├── .env                # Environment variables (create this)
├── .env.example        # Environment template
├── local_requirements.txt  # Python dependencies
├── templates/          # HTML templates
├── static/            # CSS, JS, images
└── LOCAL_SETUP.md     # This file
```