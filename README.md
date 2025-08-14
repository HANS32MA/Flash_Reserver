# 🏟️ Flash Reserver - Sistema de Reservas de Canchas Deportivas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-red.svg)](https://sqlalchemy.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-purple.svg)](https://getbootstrap.com)

## 📋 Descripción del Proyecto

**Flash Reserver** es una aplicación web completa para la gestión y reserva de canchas deportivas. El sistema permite a los usuarios registrarse, explorar canchas disponibles, realizar reservas y participar en un foro comunitario. Los administradores pueden gestionar canchas, usuarios, reservas y generar reportes detallados.

### 🎯 Características Principales

- **Sistema de Reservas**: Calendario interactivo para reservar canchas
- **Panel de Administración**: Gestión completa de usuarios, canchas y reservas
- **Sistema de Foro**: Comunidad para compartir experiencias y contenido multimedia
- **Reportes Avanzados**: Generación de PDFs y Excel con estadísticas detalladas
- **Interfaz Responsive**: Diseño moderno y adaptable a todos los dispositivos
- **Sistema de Autenticación**: Seguridad robusta con recuperación de contraseñas
- **Inicio de sesión con Google**: OAuth 2.0 con guardado de foto de perfil
- **Sistema de Configuración en Tiempo Real**: Configuraciones dinámicas sin recargar página
- **Gestión de Perfiles Avanzada**: Subida de imágenes y configuración personalizada
- **Alertas Personalizadas**: Sistema de notificaciones moderno tipo SweetAlert
- **Sistema de Notificaciones Automáticas**: Emails, recordatorios y notificaciones en tiempo real
- **Recordatorios Inteligentes**: Recordatorios automáticos 24h y 2h antes de cada reserva

## 📊 Estado del Proyecto

### ✅ **Progreso General: 95% Completado**

| Módulo | Progreso | Estado |
|--------|----------|--------|
| **Sistema de Autenticación** | 100% | ✅ Completado |
| **Gestión de Canchas** | 95% | ✅ Completado |
| **Sistema de Reservas** | 95% | ✅ Completado |
| **Panel de Administración** | 95% | ✅ Completado |
| **Sistema de Foro** | 85% | ✅ Completado |
| **Frontend y UI/UX** | 95% | ✅ Completado |
| **Utilidades y Reportes** | 95% | ✅ Completado |
| **Sistema de Configuración** | 100% | ✅ Completado |
| **Sistema de Notificaciones** | 95% | ✅ Completado |
| **Sistema de Pagos** | 0% | ❌ Pendiente |
| **API REST** | 0% | ❌ Pendiente |
| **Sistema de Calificaciones** | 0% | ❌ Pendiente |

## 🚀 Funcionalidades Implementadas

### 🔐 Sistema de Autenticación (100%)
- ✅ Registro de usuarios con validación
- ✅ Login seguro con sesiones
- ✅ Recuperación de contraseña por email
- ✅ Gestión de perfiles de usuario
- ✅ Decoradores de autorización por roles
- ✅ Tokens de seguridad para operaciones críticas
- ✅ Cambio de contraseña
- ✅ Verificación de email
- ✅ Inicio de sesión con Google (OAuth 2.0)
  - Botón en `auth/login` y `auth/register`
  - Creación automática de usuario con rol `Cliente`
  - Guardado automático de foto de perfil en `static/uploads/perfiles/`

### 🏟️ Gestión de Canchas (95%)
- ✅ CRUD completo de canchas deportivas
- ✅ Categorías y tipos de cancha
- ✅ Subida y gestión de imágenes
- ✅ Descripciones detalladas
- ✅ Horarios de disponibilidad
- ✅ Estados de cancha (activa/inactiva)
- ✅ Precios por hora
- ✅ Ubicación y detalles técnicos

### 📅 Sistema de Reservas (95%)
- ✅ Creación de reservas con validación
- ✅ Calendario de disponibilidad en tiempo real
- ✅ Historial completo de reservas
- ✅ Estados de reserva (pendiente, confirmada, cancelada)
- ✅ Gestión de horarios disponibles
- ✅ Validación de conflictos de horario
- ✅ Vista de mis reservas para usuarios
- ✅ Cancelación de reservas
- ✅ **Recordatorios automáticos** (24h y 2h antes)
- ✅ **Programación automática** de recordatorios al crear reservas
- ✅ **Cancelación automática** de recordatorios al cancelar reservas

### 👨‍💼 Panel de Administración (95%)
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Gestión completa de usuarios
- ✅ Gestión de canchas y categorías
- ✅ Administración de reservas
- ✅ Reportes en PDF y Excel
- ✅ Gestión de contenido del foro
- ✅ Estadísticas detalladas
- ✅ Configuración del sistema

### 💬 Sistema de Foro (85%)
- ✅ Creación y edición de posts
- ✅ Sistema de comentarios
- ✅ Subida de archivos multimedia
- ✅ Moderación de contenido
- ✅ Estadísticas del foro
- ✅ Categorización de posts
- ✅ Búsqueda de contenido
- ✅ Gestión de usuarios del foro

### 🎨 Frontend y UI/UX (95%)
- ✅ Diseño responsive con Bootstrap 5
- ✅ CSS moderno y atractivo
- ✅ JavaScript funcional para interacciones
- ✅ Sistema de alertas personalizadas tipo SweetAlert
- ✅ Navegación intuitiva
- ✅ Formularios validados
- ✅ Tablas interactivas
- ✅ Modales y popups
- ✅ Configuraciones en tiempo real con AJAX
- ✅ Previsualización de imágenes
- ✅ Validación en tiempo real
- ✅ Auto-guardado de preferencias

### 📊 Utilidades y Reportes (95%)
- ✅ Generación de PDFs profesionales
- ✅ Exportación a Excel
- ✅ Filtros avanzados de búsqueda
- ✅ Logs del sistema
- ✅ Estadísticas detalladas
- ✅ Gráficos y visualizaciones
- ✅ Reportes personalizables
- ✅ Backup de datos

### ⚙️ Sistema de Configuración (100%)
- ✅ **Configuración de Perfil Personal**
  - Subida y cambio de foto de perfil
  - Actualización de datos personales en tiempo real
  - Validación de email único
  - Previsualización inmediata de imágenes
  - Manejo robusto de errores de carga

- ✅ **Configuración de Seguridad**
  - Cambio de contraseña con validación en tiempo real
  - Verificación de contraseña actual
  - Validación de coincidencia de contraseñas
  - Feedback inmediato de errores

- ✅ **Configuración de Notificaciones**
  - Configuración de notificaciones push
  - Solicitud de permisos del navegador
  - Toggles de configuración en tiempo real
  - Preferencias de email y push

- ✅ **Configuración de Preferencias**
  - Idioma, zona horaria, moneda
  - Tema de interfaz (claro/oscuro/automático)
  - Configuración de sonidos
  - Guardado automático de preferencias

- ✅ **Configuración de Privacidad**
  - Visibilidad del perfil
  - Configuración de búsqueda
  - Datos personales visibles
  - Descarga de datos personales

- ✅ **Configuración del Sistema (Admin)**
  - Configuración general del sitio
  - Gestión de reservas
  - Configuración de notificaciones del sistema
  - Backup y restauración
  - Perfil personal del administrador

- ✅ **Funcionalidades Avanzadas**
  - Auto-guardado en tiempo real (2 segundos de inactividad)
  - localStorage para persistencia local
  - Envío AJAX sin recarga de página
  - Sistema de alertas personalizadas
  - Validación en tiempo real
  - Manejo robusto de errores

### 📧 Sistema de Notificaciones (95%)
- ✅ **Emails automáticos de confirmación** con plantillas personalizadas
- ✅ **Recordatorios automáticos** programados inteligentemente
- ✅ **Notificaciones en tiempo real** via WebSockets
- ✅ **Plantillas de email personalizables** con diseño moderno
- ✅ **Sistema de recordatorios inteligente** (24h y 2h antes)
- ✅ **Programación automática** de recordatorios
- ✅ **Cancelación automática** de recordatorios
- ✅ **Plantillas diferenciadas** para confirmaciones y cancelaciones
- ✅ **Diseño responsive** para emails
- ✅ **Integración completa** con el sistema de reservas

#### 🎨 Plantillas de Email Implementadas:
- **Confirmación de Reserva**: Diseño verde/azul con información detallada
- **Cancelación de Reserva**: Diseño rojo con información de reembolso
- **Recordatorio 24h**: Diseño amarillo/naranja con tips de preparación
- **Recordatorio 2h (Urgente)**: Diseño rojo con animación y acción inmediata

#### ⏰ Sistema de Recordatorios Automáticos:
- **Recordatorio 24h antes**: Email + notificación in-app con tips de preparación
- **Recordatorio 2h antes**: Email urgente + notificación in-app con acción inmediata
- **Programación automática**: Se programa al crear/confirmar reservas
- **Cancelación automática**: Se cancela al cancelar reservas
- **Scheduler inteligente**: APScheduler para gestión automática de jobs
- **Limpieza automática**: Elimina recordatorios para reservas pasadas

#### 🔧 Características Técnicas:
- **APScheduler**: Programación automática de recordatorios
- **Flask-Mail**: Envío de emails con plantillas HTML personalizadas
- **WebSockets**: Notificaciones en tiempo real
- **Base de datos**: Almacenamiento de historial de notificaciones
- **Logging**: Sistema completo de logs para debugging
- **Manejo de errores**: Reintentos automáticos y fallback

## ❌ Funcionalidades Pendientes

### 💳 Sistema de Pagos (0%)
- ❌ Integración con pasarelas de pago (Stripe/PayPal)
- ❌ Facturación electrónica
- ❌ Historial de transacciones
- ❌ Sistema de reembolsos
- ❌ Pagos recurrentes
- ❌ Cupones y descuentos

### 🔌 API REST (0%)
- ❌ Endpoints para aplicación móvil
- ❌ Documentación de API
- ❌ Autenticación JWT
- ❌ Rate limiting
- ❌ Versionado de API

### ⭐ Sistema de Calificaciones (0%)
- ❌ Reviews de canchas
- ❌ Sistema de estrellas
- ❌ Comentarios de usuarios
- ❌ Moderation de reviews
- ❌ Promedios y estadísticas

### 🔍 Características Avanzadas (0%)
- ❌ Búsqueda avanzada con filtros
- ❌ Recomendaciones personalizadas
- ❌ Sistema de lealtad
- ❌ Geolocalización
- ❌ Reservas recurrentes

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal
- **Flask 2.0+**: Framework web
- **SQLAlchemy**: ORM para base de datos
- **Flask-Login**: Gestión de sesiones
- **Flask-Mail**: Envío de emails
- **Flask-Migrate**: Migraciones de base de datos
- **Flask-SocketIO**: WebSockets para notificaciones en tiempo real
- **APScheduler**: Programación automática de tareas
- **Werkzeug**: Utilidades de seguridad

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos y animaciones
- **Bootstrap 5**: Framework CSS responsive
- **JavaScript**: Interactividad del cliente
- **Chart.js**: Gráficos y visualizaciones
- **AJAX**: Comunicación asíncrona con el servidor
- **localStorage**: Persistencia local de datos
- **FileReader API**: Previsualización de imágenes
- **WebSockets**: Comunicación en tiempo real

### Base de Datos
- **MySQL**: Base de datos principal con MySQL Workbench
- **SQLite**: Para desarrollo local
- **MySQL Workbench**: Herramienta de gestión de base de datos
- **Alembic**: Migraciones de base de datos

### Utilidades
- **ReportLab**: Generación de PDFs
- **openpyxl**: Exportación a Excel
- **Pillow**: Procesamiento de imágenes
- **python-dotenv**: Variables de entorno
- **Authlib**: Cliente OAuth 2.0 para Google
- **Requests**: Descarga de foto de perfil de Google
- **Blinker**: Sistema de señales para notificaciones

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- MySQL Server
- MySQL Workbench

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/flash-reserver.git
cd flash-reserver
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar MySQL**
```bash
# Instalar MySQL Server y MySQL Workbench
# Crear base de datos: flash_reserver
# Crear usuario con permisos
```

5. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones de MySQL y email
```

6. **Inicializar la base de datos**
```bash
flask db init
flask db migrate
flask db upgrade
```

7. **Ejecutar la aplicación**
```bash
   python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

### Configurar inicio de sesión con Google (OAuth 2.0)

1. Ve a `Google Cloud Console` → APIs y servicios → Pantalla de consentimiento OAuth.
   - Tipo de usuario: External
   - Completa nombre de app y correos.
   - Agrega tus cuentas como Test users si la app está en Testing.

2. Crea credenciales → ID de cliente de OAuth → Tipo: Aplicación web.
   - Orígenes autorizados de JavaScript:
     - `http://127.0.0.1:5000`
     - (opcional) `http://localhost:5000`
   - URIs de redirección autorizados:
     - `http://127.0.0.1:5000/auth/google/callback`
     - (opcional) `http://localhost:5000/auth/google/callback`

3. Copia el Client ID y Client Secret en tu `.env`:
```env
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret
```

4. Instala dependencias y reinicia la app:
```bash
pip install -r requirements.txt
flask run
```

5. Prueba el botón "Continuar con Google" en la pantalla de login o registro.

### Configurar Sistema de Notificaciones

1. **Configurar email en `.env`:**
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password
```

2. **El sistema se inicializa automáticamente** al arrancar Flask
3. **Los recordatorios se programan automáticamente** al crear reservas
4. **No es necesario ejecutar scripts manuales** después de la primera vez
   **Script iniciarlo una vez** python init_recordatorios.py  

## 🚀 Uso

### Para Usuarios
1. **Registro**: Crear una cuenta en `/register`
2. **Explorar Canchas**: Ver canchas disponibles en `/canchas`
3. **Hacer Reserva**: Seleccionar cancha y horario
4. **Participar en Foro**: Crear posts y comentarios
5. **Gestionar Reservas**: Ver historial en `/mis-reservas`
6. **Configurar Perfil**: Personalizar configuración en `/client/configuracion`
   - Cambiar foto de perfil
   - Actualizar datos personales
   - Configurar preferencias
   - Gestionar privacidad
   - Cambiar contraseña
7. **Recibir Notificaciones**: 
   - Email de confirmación inmediato
   - Recordatorio 24h antes de la reserva
   - Recordatorio urgente 2h antes de la reserva
   - Notificaciones in-app en tiempo real

### Para Administradores
1. **Dashboard**: Estadísticas generales en `/admin`
2. **Gestión de Usuarios**: Administrar usuarios en `/admin/usuarios`
3. **Gestión de Canchas**: Gestionar canchas en `/admin/canchas`
4. **Reportes**: Generar reportes en `/admin/reportes`
5. **Foro**: Moderar contenido en `/admin/foro`
6. **Configuración del Sistema**: Gestionar configuración en `/admin/configuracion`
   - Configuración general del sitio
   - Gestión de reservas
   - Configuración de notificaciones
   - Backup y restauración
   - Perfil personal del administrador
7. **Monitorear Notificaciones**: Ver historial de notificaciones enviadas

## 📁 Estructura del Proyecto

```
flash-reserver/
├── app/
│   ├── __init__.py
│   ├── models/           # Modelos de base de datos
│   │   ├── notificacion.py  # Modelo de notificaciones
│   │   └── ...
│   ├── routes/           # Rutas de la aplicación
│   ├── templates/        # Plantillas HTML
│   │   ├── emails/       # Plantillas de email
│   │   │   ├── recordatorio_24h.html
│   │   │   ├── recordatorio_2h.html
│   │   │   └── ...
│   │   └── ...
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   ├── forms/            # Formularios Flask-WTF
│   ├── auth/             # Autenticación y autorización
│   ├── utils/            # Utilidades y helpers
│   └── services/         # Lógica de negocio
│       ├── notificacion_service.py    # Servicio de notificaciones
│       ├── recordatorio_service.py    # Servicio de recordatorios
│       ├── websocket_service.py       # Servicio de WebSockets
│       └── scheduler_service.py       # Servicio de programación
├── migrations/           # Migraciones de base de datos
├── instance/             # Archivos de instancia
├── app.py               # Punto de entrada
├── config.py            # Configuración
├── requirements.txt     # Dependencias
├── init_recordatorios.py # Script de inicialización (opcional)
└── README.md           # Este archivo
```

## 🔧 Configuración

### Características Técnicas Avanzadas

#### 🚀 Sistema de Configuración en Tiempo Real
- **Auto-guardado**: Los cambios se guardan automáticamente después de 2 segundos de inactividad
- **localStorage**: Persistencia local para evitar pérdida de datos
- **AJAX**: Comunicación asíncrona sin recarga de página
- **Validación en tiempo real**: Validación instantánea de formularios
- **Manejo de errores**: Sistema robusto de manejo de errores de red

#### 🎨 Sistema de Alertas Personalizadas
- **Diseño moderno**: Alertas tipo SweetAlert con animaciones suaves
- **Tipos de alerta**: Success, Error, Warning, Info, Confirm
- **Confirmaciones dobles**: Para acciones críticas como eliminar cuenta
- **Personalización**: Colores, iconos y mensajes personalizados
- **Responsive**: Funciona perfectamente en móviles

#### 📸 Gestión de Imágenes Avanzada
- **Previsualización**: Vista previa inmediata al seleccionar imagen
- **Validación**: Verificación de tipo y tamaño de archivo
- **Optimización**: Redimensionamiento automático si es necesario
- **Fallback**: Imagen por defecto si hay errores de carga
- **Seguridad**: Nombres de archivo seguros y validación de contenido

#### ⚡ Funcionalidades de UX
- **Estados de carga**: Indicadores visuales durante operaciones
- **Feedback inmediato**: Notificaciones instantáneas de éxito/error
- **Navegación fluida**: Transiciones suaves entre secciones
- **Responsive design**: Adaptación perfecta a todos los dispositivos
- **Accesibilidad**: Soporte para teclado y lectores de pantalla

#### 📧 Sistema de Notificaciones Avanzado
- **Plantillas personalizadas**: Diseños únicos para cada tipo de notificación
- **Recordatorios inteligentes**: Programación automática basada en fechas de reserva
- **Scheduler automático**: APScheduler para gestión de tareas programadas
- **WebSockets**: Notificaciones en tiempo real sin recarga
- **Manejo de errores**: Reintentos automáticos y fallback
- **Logging completo**: Sistema de logs para debugging y monitoreo

### Variables de Entorno (.env)
```env
SECRET_KEY=tu-clave-secreta
DATABASE_URI=mysql+pymysql://usuario:password@localhost/flash_reserver
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password
FLASK_ENV=development
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret

# Configuración de Notificaciones
NOTIFICACIONES_EMAIL_ENABLED=True
NOTIFICACIONES_PUSH_ENABLED=True
NOTIFICACIONES_SMS_ENABLED=False
NOTIFICACIONES_IN_APP_ENABLED=True

# Configuración de WebSockets
SOCKETIO_ASYNC_MODE=threading
SOCKETIO_CORS_ALLOWED_ORIGINS=http://127.0.0.1:5000

# Configuración del Scheduler
SCHEDULER_ENABLED=True
SCHEDULER_TIMEZONE=UTC
```

### Configuración de Base de Datos
- **Desarrollo**: MySQL con MySQL Workbench
- **Producción**: MySQL con optimizaciones
- **Local**: SQLite para pruebas rápidas

## 🧪 Testing

```bash
# Ejecutar tests unitarios
python -m pytest tests/

# Ejecutar tests con cobertura
python -m pytest --cov=app tests/

# Probar sistema de notificaciones
python init_recordatorios.py
```

## 📈 Roadmap de Desarrollo

### Fase 1: Completar Core (95-98%)
- [ ] **Sistema de Pagos**
  - Integrar Stripe/PayPal
  - Implementar facturación
  - Historial de transacciones
- [ ] **Optimizaciones Finales**
  - Mejorar rendimiento de notificaciones
  - Optimizar base de datos
  - Cache de plantillas de email

### Fase 2: Funcionalidades Avanzadas (98-99%)
- [ ] **Sistema de Calificaciones**
  - Reviews de canchas
  - Sistema de estrellas
  - Moderation de contenido
- [ ] **Búsqueda y Filtros Avanzados**
  - Filtros por precio, ubicación, tipo
  - Búsqueda geolocalizada
  - Recomendaciones

### Fase 3: Expansión (99-100%)
- [ ] **API REST**
  - Endpoints para móvil
  - Documentación completa
  - Autenticación JWT
- [ ] **Características Premium**
  - Sistema de lealtad
  - Cupones y descuentos
  - Reservas recurrentes

## 🔒 Seguridad

- ✅ Validación de entrada en formularios
- ✅ Protección CSRF
- ✅ Hashing seguro de contraseñas
- ✅ Gestión de sesiones segura
- ✅ Decoradores de autorización
- ✅ Sanitización de datos
- ✅ OAuth 2.0 con Google y manejo de redirecciones seguro
- ✅ Validación de emails y notificaciones
- ✅ Rate limiting para notificaciones
- ✅ Logging de seguridad para notificaciones

### Solución de problemas (Google OAuth)
- `invalid_client`: el `GOOGLE_CLIENT_ID` no coincide con el de tu credencial "Aplicación web". Revisa `.env` y reinicia.
- `redirect_uri_mismatch`: agrega exactamente `http://127.0.0.1:5000/auth/google/callback` en tu cliente OAuth.
- Vuelve a intentar en incógnito si ves mensajes de CSP o de cookies de terceros; son informativos y no bloquean el flujo.

### Solución de problemas (Notificaciones)
- **Emails no se envían**: Verifica configuración SMTP en `.env`
- **Recordatorios no se programan**: Verifica que APScheduler esté funcionando
- **WebSockets no funcionan**: Verifica configuración de CORS y async mode

## 📊 Métricas del Proyecto

- **Líneas de código**: ~22,000+
- **Archivos**: 130+
- **Funcionalidades**: 40+
- **Templates**: 50+
- **Rutas**: 65+
- **Secciones de configuración**: 6 (Perfil, Seguridad, Notificaciones, Preferencias, Privacidad, Sistema)
- **Alertas personalizadas**: 5 tipos (Success, Error, Warning, Info, Confirm)
- **Funciones JavaScript**: 30+ funciones especializadas
- **Plantillas de email**: 4 tipos (Confirmación, Cancelación, Recordatorio 24h, Recordatorio 2h)
- **Servicios implementados**: 4 (Notificaciones, Recordatorios, WebSockets, Scheduler)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Hans Sebastian**
- Email: hanssebastianmirandaarrieta@gmail.com
- GitHub: [@HANS32MA](https://github.com/HANS32MA)

## 🙏 Agradecimientos

- Flask y su comunidad
- Bootstrap por el framework CSS
- APScheduler por el sistema de programación
- Flask-Mail por el sistema de emails
- Todos los contribuidores del proyecto

## 📞 Soporte

Si tienes alguna pregunta o necesitas ayuda:
- Abre un issue en GitHub
- Contacta al desarrollador
- Revisa la documentación

---

**Flash Reserver** - Haciendo las reservas deportivas más fáciles y eficientes 🏟️⚽

## 🎉 **¡NUEVO! Sistema de Notificaciones Completamente Implementado**

### ✨ **Características Destacadas:**
- **📧 Emails automáticos** con plantillas profesionales
- **⏰ Recordatorios inteligentes** (24h y 2h antes)
- **🚨 Notificaciones urgentes** con diseño diferenciado
- **🔄 Programación automática** sin intervención manual
- **🎨 Plantillas personalizadas** para cada tipo de notificación
- **⚡ Sistema en tiempo real** con WebSockets
- **🧠 Scheduler inteligente** para gestión automática

### 🚀 **¿Cómo Funciona?**
1. **Crear reserva** → Recordatorios se programan automáticamente
2. **Confirmar reserva** → Email de confirmación inmediato
3. **24h antes** → Recordatorio con tips de preparación
4. **2h antes** → Recordatorio urgente con acción inmediata
5. **Cancelar reserva** → Recordatorios se cancelan automáticamente

### 💡 **Beneficios:**
- ✅ **Reduce cancelaciones** de último momento
- ✅ **Mejora la experiencia** del usuario
- ✅ **Aumenta la asistencia** a las reservas
- ✅ **Comunicación proactiva** con los clientes
- ✅ **Sistema completamente automático**

**¡El sistema ya está funcionando perfectamente! 🎯**
