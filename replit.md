# Skill Swap Platform

## Overview

The Skill Swap Platform is a web-based application that enables users to exchange skills with one another. Built with Flask and SQLAlchemy, it provides a comprehensive platform for users to list their offered skills, specify wanted skills, and arrange skill exchanges with other platform members.

## User Preferences

Preferred communication style: Simple, everyday language.

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