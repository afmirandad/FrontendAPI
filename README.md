# Frontend API - Sistema de Autenticación

Frontend web desarrollado en Python con Flask que se conecta a la API de usuarios. Incluye un sistema de autenticación con JWT y un diseño moderno con partículas interconectadas en el fondo.

## 🌟 Características

- ✅ **Sistema de Login y Registro** - Autenticación completa de usuarios
- 🔐 **Protección JWT** - Rutas protegidas con tokens JWT
- 🎨 **Theme de Partículas Interconectadas** - Fondo animado con red de partículas
- 📝 **Logging Completo** - Sistema de logs sin prints en consola
- 🔒 **Variables de Entorno** - Configuración segura con archivos .env
- 📱 **Diseño Responsive** - Compatible con dispositivos móviles
- ⚡ **Validación en Tiempo Real** - Formularios con validación interactiva

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask 3.0.3
- **HTTP Client**: Requests 2.32.3
- **JWT**: PyJWT 2.9.0
- **Environment**: python-dotenv 1.0.1
- **Server**: Gunicorn 23.0.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd FrontendAPI
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y personaliza las variables:

```env
# Flask Configuration
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
FLASK_ENV=development
FLASK_DEBUG=True

# API Configuration
API_BASE_URL=https://flaskapiexample-production.up.railway.app

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

## ▶️ Ejecución

### Modo Desarrollo

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Modo Producción con Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Donde:
- `-w 4`: 4 workers (ajustar según CPU)
- `-b 0.0.0.0:5000`: Bind a todas las interfaces en el puerto 5000

## 📁 Estructura del Proyecto

```
FrontendAPI/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Variables de entorno (no en git)
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados por git
├── README.md                  # Este archivo
├── logs/                      # Directorio de logs (creado automáticamente)
│   └── app.log               # Archivo de logs
├── templates/                 # Plantillas HTML
│   ├── base.html             # Template base
│   ├── login.html            # Página de login
│   ├── register.html         # Página de registro
│   ├── users.html            # Página de usuarios
│   ├── 404.html              # Página de error 404
│   └── 500.html              # Página de error 500
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── styles.css        # Estilos CSS
│   └── js/
│       ├── particles.js      # Sistema de partículas
│       └── main.js           # JavaScript principal
└── venv/                      # Entorno virtual (no en git)
```

## 🎯 Endpoints de la API

La aplicación se conecta a los siguientes endpoints:

- **POST** `/users/login` - Autenticación de usuarios
- **POST** `/users/register` - Registro de nuevos usuarios
- **GET** `/users` - Obtener lista de usuarios (requiere JWT)

## 🔐 Flujo de Autenticación

1. **Registro**: El usuario se registra con nombre, email y contraseña
2. **Login**: El usuario inicia sesión con email y contraseña
3. **Token JWT**: Al hacer login exitoso, se recibe un token JWT
4. **Acceso Protegido**: El token se almacena en la sesión de Flask
5. **Validación**: Las rutas protegidas verifican el token antes de mostrar contenido
6. **Redirección**: Si no hay token válido, se redirige automáticamente al login

## 📊 Sistema de Logging

Los logs se guardan en el directorio `logs/app.log` con la siguiente información:

- Timestamp de cada evento
- Nivel de log (INFO, WARNING, ERROR)
- Mensaje descriptivo
- Archivo y línea de código

Ejemplo de logs:
```
2025-10-27 10:30:15 INFO: Frontend application startup
2025-10-27 10:30:20 INFO: Login attempt for email: user@example.com
2025-10-27 10:30:21 INFO: Successful login for user: user@example.com
```

## 🎨 Theme de Partículas

El sistema de partículas crea un fondo animado e interactivo:

- **80 partículas** flotantes con movimiento suave
- **Conexiones dinámicas** entre partículas cercanas
- **Interacción con el mouse** - las partículas reaccionan al cursor
- **Responsive** - se adapta al tamaño de la pantalla
- **Optimizado** - usa requestAnimationFrame para mejor rendimiento

## 🔧 Configuración Avanzada

### Personalizar el Sistema de Partículas

Edita `static/js/particles.js`:

```javascript
this.config = {
    particleCount: 80,              // Número de partículas
    particleSpeed: 0.5,             // Velocidad de movimiento
    particleSize: 2,                // Tamaño de las partículas
    connectionDistance: 150,        // Distancia de conexión
    mouseConnectionDistance: 200,   // Distancia de interacción con mouse
    particleColor: 'rgba(129, 140, 248, 0.8)',
    lineColor: 'rgba(99, 102, 241, 0.2)',
    mouseLineColor: 'rgba(139, 92, 246, 0.4)'
};
```

### Personalizar Colores

Edita `static/css/styles.css`:

```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --secondary-color: #8b5cf6;
    /* ... más variables */
}
```

## 🐛 Solución de Problemas

### Error de conexión con la API

**Problema**: `Error al conectar con el servidor`

**Solución**: Verifica que la API esté disponible:
```bash
curl https://flaskapiexample-production.up.railway.app/users
```

### Token JWT expirado

**Problema**: `Tu sesión ha expirado`

**Solución**: Vuelve a iniciar sesión. Los tokens tienen un tiempo de expiración.

### Puerto 5000 en uso

**Problema**: `Address already in use`

**Solución**: Cambia el puerto en `.env`:
```env
PORT=8000
```

## 📝 Notas de Desarrollo

- **No usar prints**: Todo el debug se hace con el sistema de logging
- **Seguridad**: Nunca subir el archivo `.env` al repositorio
- **Producción**: Cambiar `SECRET_KEY` y establecer `FLASK_DEBUG=False`
- **HTTPS**: En producción, usar HTTPS para proteger las credenciales

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.

## 👨‍💻 Autor

Desarrollado como frontend para la API de gestión de usuarios.

---

**¡Disfruta del proyecto! 🚀**
