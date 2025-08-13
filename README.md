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

## 📊 Estado del Proyecto

### ✅ **Progreso General: 85% Completado**

| Módulo | Progreso | Estado |
|--------|----------|--------|
| **Sistema de Autenticación** | 100% | ✅ Completado |
| **Gestión de Canchas** | 95% | ✅ Completado |
| **Sistema de Reservas** | 90% | ✅ Completado |
| **Panel de Administración** | 95% | ✅ Completado |
| **Sistema de Foro** | 85% | ✅ Completado |
| **Frontend y UI/UX** | 90% | ✅ Completado |
| **Utilidades y Reportes** | 95% | ✅ Completado |
| **Sistema de Pagos** | 0% | ❌ Pendiente |
| **Notificaciones** | 20% | 🔄 En Progreso |
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

### 🏟️ Gestión de Canchas (95%)
- ✅ CRUD completo de canchas deportivas
- ✅ Categorías y tipos de cancha
- ✅ Subida y gestión de imágenes
- ✅ Descripciones detalladas
- ✅ Horarios de disponibilidad
- ✅ Estados de cancha (activa/inactiva)
- ✅ Precios por hora
- ✅ Ubicación y detalles técnicos

### 📅 Sistema de Reservas (90%)
- ✅ Creación de reservas con validación
- ✅ Calendario de disponibilidad en tiempo real
- ✅ Historial completo de reservas
- ✅ Estados de reserva (pendiente, confirmada, cancelada)
- ✅ Gestión de horarios disponibles
- ✅ Validación de conflictos de horario
- ✅ Vista de mis reservas para usuarios
- ✅ Cancelación de reservas

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

### 🎨 Frontend y UI/UX (90%)
- ✅ Diseño responsive con Bootstrap 5
- ✅ CSS moderno y atractivo
- ✅ JavaScript funcional para interacciones
- ✅ Sistema de alertas y notificaciones
- ✅ Navegación intuitiva
- ✅ Formularios validados
- ✅ Tablas interactivas
- ✅ Modales y popups

### 📊 Utilidades y Reportes (95%)
- ✅ Generación de PDFs profesionales
- ✅ Exportación a Excel
- ✅ Filtros avanzados de búsqueda
- ✅ Logs del sistema
- ✅ Estadísticas detalladas
- ✅ Gráficos y visualizaciones
- ✅ Reportes personalizables
- ✅ Backup de datos

## ❌ Funcionalidades Pendientes

### 💳 Sistema de Pagos (0%)
- ❌ Integración con pasarelas de pago (Stripe/PayPal)
- ❌ Facturación electrónica
- ❌ Historial de transacciones
- ❌ Sistema de reembolsos
- ❌ Pagos recurrentes
- ❌ Cupones y descuentos

### 📧 Notificaciones (20%)
- ❌ Emails automáticos de confirmación
- ❌ Notificaciones push
- ❌ SMS de recordatorio
- ❌ Notificaciones en tiempo real
- ❌ Plantillas de email personalizables

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
- **Werkzeug**: Utilidades de seguridad

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos y animaciones
- **Bootstrap 5**: Framework CSS responsive
- **JavaScript**: Interactividad del cliente
- **Chart.js**: Gráficos y visualizaciones

### Base de Datos
- **MySQL**: Base de datos principal con MySQL Workbench
- **SQLite**: Para desarrollo local
- **MySQL Workbench**: Herramienta de gestión de base de datos

### Utilidades
- **ReportLab**: Generación de PDFs
- **openpyxl**: Exportación a Excel
- **Pillow**: Procesamiento de imágenes
- **python-dotenv**: Variables de entorno

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
# Editar .env con tus configuraciones de MySQL
```

6. **Inicializar la base de datos**
```bash
flask db init
flask db migrate
flask db upgrade
```

7. **Ejecutar la aplicación**
```bash
flask run
```

La aplicación estará disponible en `http://localhost:5000`

## 🚀 Uso

### Para Usuarios
1. **Registro**: Crear una cuenta en `/register`
2. **Explorar Canchas**: Ver canchas disponibles en `/canchas`
3. **Hacer Reserva**: Seleccionar cancha y horario
4. **Participar en Foro**: Crear posts y comentarios
5. **Gestionar Reservas**: Ver historial en `/mis-reservas`

### Para Administradores
1. **Dashboard**: Estadísticas generales en `/admin`
2. **Gestión de Usuarios**: Administrar usuarios en `/admin/usuarios`
3. **Gestión de Canchas**: Gestionar canchas en `/admin/canchas`
4. **Reportes**: Generar reportes en `/admin/reportes`
5. **Foro**: Moderar contenido en `/admin/foro`

## 📁 Estructura del Proyecto

```
flash-reserver/
├── app/
│   ├── __init__.py
│   ├── models/           # Modelos de base de datos
│   ├── routes/           # Rutas de la aplicación
│   ├── templates/        # Plantillas HTML
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   ├── forms/            # Formularios Flask-WTF
│   ├── auth/             # Autenticación y autorización
│   ├── utils/            # Utilidades y helpers
│   └── services/         # Lógica de negocio
├── migrations/           # Migraciones de base de datos
├── instance/             # Archivos de instancia
├── app.py               # Punto de entrada
├── config.py            # Configuración
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (.env)
```env
SECRET_KEY=tu-clave-secreta
DATABASE_URI=mysql+pymysql://usuario:password@localhost/flash_reserver
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-password
FLASK_ENV=development
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
```

## 📈 Roadmap de Desarrollo

### Fase 1: Completar Core (90-95%)
- [ ] **Sistema de Pagos**
  - Integrar Stripe/PayPal
  - Implementar facturación
  - Historial de transacciones
- [ ] **Notificaciones Automáticas**
  - Emails de confirmación
  - Recordatorios de reserva
  - Notificaciones de estado

### Fase 2: Funcionalidades Avanzadas (95-98%)
- [ ] **Sistema de Calificaciones**
  - Reviews de canchas
  - Sistema de estrellas
  - Moderation de contenido
- [ ] **Búsqueda y Filtros Avanzados**
  - Filtros por precio, ubicación, tipo
  - Búsqueda geolocalizada
  - Recomendaciones

### Fase 3: Expansión (98-100%)
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

## 📊 Métricas del Proyecto

- **Líneas de código**: ~15,000+
- **Archivos**: 100+
- **Funcionalidades**: 25+
- **Templates**: 40+
- **Rutas**: 50+

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
- Todos los contribuidores del proyecto

## 📞 Soporte

Si tienes alguna pregunta o necesitas ayuda:
- Abre un issue en GitHub
- Contacta al desarrollador
- Revisa la documentación

---

**Flash Reserver** - Haciendo las reservas deportivas más fáciles y eficientes 🏟️⚽



















































































































                                                            ⠄⠄⠄⠄⠄⠄
                                                        ⣿⠛⠛⠉⠄⠁⠄⠄⠉⠛⢿
                                                      ⡟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
                                                     ⣿⡇⠄⠄⠄⠐⠄⠄⠄⠄⠄⠄⠄⠠⣿
                                                     ⣿⡇⠄⢀⡀⠠⠃⡐⡀⠠⣶⠄⠄⢀⣿
                                                      ⣶⠄⠰⣤⣕⣿⣾⡇⠄⢛⠃⠄⢈⣿
                                                      ⣿⡇⢀⣻⠟⣻⣿⡇⠄⠧⠄⢀⣾⣿
                                                        ⣟⢸⣻⣭⡙⢄⢀⠄⠄⠄⠈⢹⣯
                                                       ⣿⣭⣿⣿⣿⣧⢸⠄⠄BYE⠈⢸
       **¡Disfruta usando FlashReseerver! ⚽🏀🎾**  ⣿⣼⣿⣿⣿⣽⠘⡄⠄⠄⠄⠄⢀⠸
                                                     ⣿⣳⣿⣿⣿⣿⣿⠄⠓⠦⠤⠤⠤⠼⢸
                                                    ⡹⣧⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⢇⣓
                                                    ⡞⣸⣿⣿⢏⣼⣶⣶⣶⣶⣤⣶⡤⠐⣿
                                                    ⣯⣽⣛⠅⣾⣿⣿⣿⣿⣿⡽⣿⣧⡸⢿
                                                        ⡷⠹⠛⠉⠁⠄⠄⠄⠄⠄⠄⠐⠛⠻⣿
                                                       ⣿⠃⠄⠄⠄⠄⠄⣠⣤⣤⣤⡄⢤⣤⣤⣤⡘⠻
                                                       ⡟⠄⠄⣀⣤⣶⣿⣿⣿⣿⣿⣿⣆⢻⣿⣿⣿⡎⠝
                                                     ⡏⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⠐
                                                     ⡏⣲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⡟⣼
                                                    ⣿⡠⠜⣿⣿⣿⣿⣟⡛⠿⠿⠿⠿⠟⠃⠾⠿⢟⡋⢶
                                                     ⣧⣄⠙⢿⣿⣿⣿⣿⣿⣷⣦⡀⢰⣾⣿⣿⡿⢣⣿
                                                      ⣿⠂⣷⣶⣬⣭⣭⣭⣭⣵⢰⣴⣤⣤⣶⡾⢐⣿
                                                       ⣷⡘⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⢃⣼