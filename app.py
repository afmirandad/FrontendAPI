"""
Frontend application for API authentication and user management.
"""
import os
import logging
from functools import wraps
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import requests
import jwt

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-for-sessions-12345')

# Session configuration - simplified
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://flaskapiexample-production.up.railway.app')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))

app.logger.addHandler(file_handler)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Frontend application startup')


def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app.logger.info(f'login_required check - session contents: {dict(session)}')
        app.logger.info(f'login_required check - has token: {"token" in session}')
        if 'token' not in session:
            app.logger.warning('Unauthorized access attempt to protected route - no token in session')
            flash('Por favor inicia sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        app.logger.info('login_required check passed')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Redirect to login or users page depending on authentication status."""
    app.logger.info('Index page accessed')
    if 'token' in session:
        return redirect(url_for('users'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication handler."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        app.logger.info(f'Login attempt for username: {username}')
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/users/login',
                json={'username': username, 'password': password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                
                # Debug logging
                app.logger.info(f'API response data: {data}')
                app.logger.info(f'Access token type: {type(access_token)}')
                app.logger.info(f'Access token value: {access_token}')
                
                if access_token:
                    session['token'] = access_token
                    session.permanent = True  # Make session permanent
                    app.logger.info(f'Token stored in session: {session.get("token", "NOT FOUND")}')
                    app.logger.info(f'Session contents: {dict(session)}')
                else:
                    app.logger.error('No access_token found in API response')
                    flash('Error: No se recibió token de acceso', 'error')
                    return render_template('login.html')
                
                app.logger.info(f'Successful login for user: {username}')
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('users'))
            else:
                error_message = response.json().get('message', 'Error en el inicio de sesión')
                app.logger.warning(f'Failed login attempt for {username}: {error_message}')
                flash(error_message, 'error')
        except requests.exceptions.RequestException as e:
            app.logger.error(f'API request error during login: {str(e)}')
            flash('Error al conectar con el servidor. Por favor intenta de nuevo.', 'error')
        except Exception as e:
            app.logger.error(f'Unexpected error during login: {str(e)}')
            flash('Error inesperado. Por favor intenta de nuevo.', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        app.logger.info(f'Registration attempt for username: {username}')
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/users/register',
                json={'username': username, 'password': password},
                timeout=10
            )
            
            if response.status_code == 201:
                app.logger.info(f'Successful registration for user: {username}')
                flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
                return redirect(url_for('login'))
            else:
                error_message = response.json().get('message', 'Error en el registro')
                app.logger.warning(f'Failed registration attempt for {username}: {error_message}')
                flash(error_message, 'error')
        except requests.exceptions.RequestException as e:
            app.logger.error(f'API request error during registration: {str(e)}')
            flash('Error al conectar con el servidor. Por favor intenta de nuevo.', 'error')
        except Exception as e:
            app.logger.error(f'Unexpected error during registration: {str(e)}')
            flash('Error inesperado. Por favor intenta de nuevo.', 'error')
    
    return render_template('register.html')


@app.route('/users')
@login_required
def users():
    """Display users page with user list from API."""
    app.logger.info('Users page accessed')
    
    try:
        # Get authorization token from session
        app.logger.info(f'Full session contents: {dict(session)}')
        app.logger.info(f'Session keys: {list(session.keys())}')
        
        try:
            direct_token = session['token']
            app.logger.info(f'Direct session access successful: {direct_token}')
        except KeyError:
            app.logger.error('KeyError: token not found in session')
        
        token = session.get('token')
        app.logger.info(f'Token from session.get(): {token}')
        app.logger.info(f'Token type: {type(token)}')
        
        if not token:
            app.logger.warning('No token found in session, redirecting to login')
            flash('Tu sesión ha expirado. Por favor inicia sesión de nuevo.', 'warning')
            return redirect(url_for('login'))
        
        headers = {'Authorization': f'Bearer {token}'}
        app.logger.info(f'Request headers: {headers}')
        
        # Make request to API to get users
        response = requests.get(
            f'{API_BASE_URL}/users/',
            headers=headers,
            timeout=10
        )
        app.logger.info(f'Full API response: {'curl -i {API_BASE_URL}/users/ -H "Authorization: Bearer {token}"'}')

        app.logger.info(f'API Response status: {response.status_code}')
        app.logger.info(f'API Response body: {response.text[:200]}...')
        
        if response.status_code == 200:
            raw_users = response.json()
            app.logger.info(f'Raw API response: {raw_users}')
            
            # Process and format users data
            users_data = []
            for user in raw_users:
                formatted_user = {
                    "id": user.get("id"),
                    "username": user.get("username")
                }
                users_data.append(formatted_user)
            
            app.logger.info(f'Successfully retrieved and formatted {len(users_data)} users')
            app.logger.info(f'Formatted users: {users_data}')
            return render_template('users.html', users=users_data)
        elif response.status_code == 401:
            app.logger.warning('Token expired or invalid, redirecting to login')
            session.clear()
            flash('Tu sesión ha expirado. Por favor inicia sesión de nuevo.', 'warning')
            return redirect(url_for('login'))
        else:
            app.logger.error(f'API error when fetching users: {response.status_code}')
            flash('Error al cargar los usuarios. Por favor intenta de nuevo.', 'error')
            return render_template('users.html', users=[])
            
    except requests.exceptions.RequestException as e:
        app.logger.error(f'API request error when fetching users: {str(e)}')
        flash('Error al conectar con el servidor. Por favor intenta de nuevo.', 'error')
        return render_template('users.html', users=[])
    except Exception as e:
        app.logger.error(f'Unexpected error when fetching users: {str(e)}')
        flash('Error inesperado. Por favor intenta de nuevo.', 'error')
        return render_template('users.html', users=[])


@app.route('/electrodomesticos')
@login_required
def electrodomesticos():
    """Display electrodomesticos page with appliances list from API."""
    app.logger.info('Electrodomesticos page accessed')
    
    try:
        # Get authorization token from session
        token = session.get('token')
        
        if not token:
            app.logger.warning('No token found in session, redirecting to login')
            flash('Tu sesión ha expirado. Por favor inicia sesión de nuevo.', 'warning')
            return redirect(url_for('login'))
        
        headers = {'Authorization': f'Bearer {token}'}
        
        # Make request to API to get electrodomesticos
        response = requests.get(
            f'{API_BASE_URL}/electrodomesticos/',
            headers=headers,
            timeout=10
        )
        
        app.logger.info(f'API Response status: {response.status_code}')
        app.logger.info(f'API Response body: {response.text[:200]}...')
        
        if response.status_code == 200:
            raw_electrodomesticos = response.json()
            app.logger.info(f'Raw API response: {raw_electrodomesticos}')
            
            # Process and format electrodomesticos data
            electrodomesticos_data = []
            for item in raw_electrodomesticos:
                formatted_item = {
                    "id": item.get("id"),
                    "marca": item.get("marca"),
                    "modelo": item.get("modelo"),
                    "tipo": item.get("tipo"),
                    "precio": item.get("precio"),
                    "clase_energetica": item.get("clase_energetica"),
                    "en_stock": item.get("en_stock", False)
                }
                electrodomesticos_data.append(formatted_item)
            
            app.logger.info(f'Successfully retrieved and formatted {len(electrodomesticos_data)} electrodomesticos')
            return render_template('electrodomesticos.html', electrodomesticos=electrodomesticos_data)
        elif response.status_code == 401:
            app.logger.warning('Token expired or invalid, redirecting to login')
            session.clear()
            flash('Tu sesión ha expirado. Por favor inicia sesión de nuevo.', 'warning')
            return redirect(url_for('login'))
        else:
            app.logger.error(f'API error when fetching electrodomesticos: {response.status_code}')
            flash('Error al cargar los electrodomésticos. Por favor intenta de nuevo.', 'error')
            return render_template('electrodomesticos.html', electrodomesticos=[])
            
    except requests.exceptions.RequestException as e:
        app.logger.error(f'API request error when fetching electrodomesticos: {str(e)}')
        flash('Error al conectar con el servidor. Por favor intenta de nuevo.', 'error')
        return render_template('electrodomesticos.html', electrodomesticos=[])
    except Exception as e:
        app.logger.error(f'Unexpected error when fetching electrodomesticos: {str(e)}')
        flash('Error inesperado. Por favor intenta de nuevo.', 'error')
        return render_template('electrodomesticos.html', electrodomesticos=[])


@app.route('/debug/session')
def debug_session():
    """Debug endpoint to check session contents."""
    session_data = dict(session)
    token = session.get('token')
    return jsonify({
        'session_data': session_data,
        'has_token': token is not None,
        'token_preview': token[:20] + '...' if token else None,
        'session_id': request.cookies.get('session')
    })


@app.route('/logout')
def logout():
    """Logout handler."""
    user = session.get('user', {})
    app.logger.info(f'User logged out: {user.get("email", "unknown")}')
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    app.logger.warning(f'Page not found: {request.url}')
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f'Internal server error: {str(error)}')
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.logger.info(f'Starting Flask app on {HOST}:{PORT}')
    app.run(host=HOST, port=PORT, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
