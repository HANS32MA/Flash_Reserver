/**
 * Sistema de Alertas Personalizadas
 * Maneja alertas modernas y animadas para toda la aplicación
 */

class CustomAlerts {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Crear contenedor de alertas si no existe
        if (!document.querySelector('.alert-container')) {
            this.container = document.createElement('div');
            this.container.className = 'alert-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.alert-container');
        }
    }

    /**
     * Muestra una alerta personalizada
     * @param {string} type - Tipo de alerta (success, error, warning, info, primary)
     * @param {string} title - Título de la alerta
     * @param {string} message - Mensaje de la alerta
     * @param {number} duration - Duración en milisegundos (0 = no auto-close)
     */
    show(type, title, message, duration = 5000) {
        const alert = this.createAlert(type, title, message);
        this.container.appendChild(alert);

        // Animar entrada
        setTimeout(() => {
            alert.classList.add('show', 'animate-in');
        }, 10);

        // Auto-cerrar si se especifica duración
        if (duration > 0) {
            setTimeout(() => {
                this.hide(alert);
            }, duration);
        }

        return alert;
    }

    /**
     * Crea el elemento HTML de la alerta
     */
    createAlert(type, title, message) {
        const alert = document.createElement('div');
        alert.className = `custom-alert ${type}`;
        
        const icon = this.getIcon(type);
        
        alert.innerHTML = `
            <i class="alert-icon ${icon}"></i>
            <div class="alert-content">
                <div class="alert-title">${title}</div>
                <div class="alert-message">${message}</div>
            </div>
            <button class="alert-close" onclick="customAlerts.hide(this.parentElement)">
                <i class="fas fa-times"></i>
            </button>
        `;

        return alert;
    }

    /**
     * Obtiene el icono correspondiente al tipo de alerta
     */
    getIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle',
            primary: 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    /**
     * Oculta una alerta específica
     */
    hide(alert) {
        alert.classList.add('animate-out');
        setTimeout(() => {
            alert.classList.add('hide');
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.parentElement.removeChild(alert);
                }
            }, 300);
        }, 300);
    }

    /**
     * Oculta todas las alertas
     */
    hideAll() {
        const alerts = this.container.querySelectorAll('.custom-alert');
        alerts.forEach(alert => this.hide(alert));
    }

    /**
     * Muestra una alerta de éxito
     */
    success(title, message, duration = 5000) {
        return this.show('success', title, message, duration);
    }

    /**
     * Muestra una alerta de error
     */
    error(title, message, duration = 7000) {
        return this.show('error', title, message, duration);
    }

    /**
     * Muestra una alerta de advertencia
     */
    warning(title, message, duration = 6000) {
        return this.show('warning', title, message, duration);
    }

    /**
     * Muestra una alerta informativa
     */
    info(title, message, duration = 5000) {
        return this.show('info', title, message, duration);
    }

    /**
     * Muestra una alerta primaria
     */
    primary(title, message, duration = 5000) {
        return this.show('primary', title, message, duration);
    }

    /**
     * Muestra una alerta de confirmación personalizada
     */
    confirm(title, message, onConfirm, onCancel = null) {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'confirm-overlay';
            
            const alert = document.createElement('div');
            alert.className = 'confirm-alert';
            alert.innerHTML = `
                <div class="confirm-icon">
                    <i class="fas fa-question-circle"></i>
                </div>
                <div class="confirm-title">${title}</div>
                <div class="confirm-message">${message}</div>
                <div class="confirm-buttons">
                    <button class="btn btn-cancel">Cancelar</button>
                    <button class="btn btn-confirm">Confirmar</button>
                </div>
            `;

            overlay.appendChild(alert);
            document.body.appendChild(overlay);

            // Animar entrada
            setTimeout(() => {
                alert.style.transform = 'translate(-50%, -50%) scale(1)';
                alert.style.opacity = '1';
            }, 10);

            // Event listeners
            const confirmBtn = alert.querySelector('.btn-confirm');
            const cancelBtn = alert.querySelector('.btn-cancel');

            const closeModal = () => {
                alert.style.transform = 'translate(-50%, -50%) scale(0.8)';
                alert.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 200);
            };

            confirmBtn.addEventListener('click', () => {
                closeModal();
                if (onConfirm) onConfirm();
                resolve(true);
            });

            cancelBtn.addEventListener('click', () => {
                closeModal();
                if (onCancel) onCancel();
                resolve(false);
            });

            // Cerrar con ESC
            const handleEsc = (e) => {
                if (e.key === 'Escape') {
                    closeModal();
                    if (onCancel) onCancel();
                    resolve(false);
                    document.removeEventListener('keydown', handleEsc);
                }
            };
            document.addEventListener('keydown', handleEsc);

            // Cerrar haciendo clic en el overlay
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    closeModal();
                    if (onCancel) onCancel();
                    resolve(false);
                }
            });
        });
    }

    /**
     * Muestra una alerta de confirmación para eliminar
     */
    confirmDelete(itemName, onConfirm) {
        return this.confirm(
            'Confirmar Eliminación',
            `¿Estás seguro de que deseas eliminar "${itemName}"? Esta acción no se puede deshacer.`,
            onConfirm
        );
    }

    /**
     * Muestra una alerta de confirmación para acciones importantes
     */
    confirmAction(title, message, onConfirm) {
        return this.confirm(title, message, onConfirm);
    }
}

// Inicializar el sistema de alertas
const customAlerts = new CustomAlerts();

// Funciones de conveniencia para uso global
window.showAlert = (type, title, message, duration) => {
    return customAlerts.show(type, title, message, duration);
};

window.showSuccess = (title, message, duration) => {
    return customAlerts.success(title, message, duration);
};

window.showError = (title, message, duration) => {
    return customAlerts.error(title, message, duration);
};

window.showWarning = (title, message, duration) => {
    return customAlerts.warning(title, message, duration);
};

window.showInfo = (title, message, duration) => {
    return customAlerts.info(title, message, duration);
};

window.showConfirm = (title, message, onConfirm, onCancel) => {
    return customAlerts.confirm(title, message, onConfirm, onCancel);
};

window.showConfirmDelete = (itemName, onConfirm) => {
    return customAlerts.confirmDelete(itemName, onConfirm);
};

// Función para mostrar alertas desde Flask flash messages
window.showFlashMessages = () => {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(alert => {
        const type = alert.classList.contains('alert-success') ? 'success' :
                    alert.classList.contains('alert-danger') ? 'error' :
                    alert.classList.contains('alert-warning') ? 'warning' :
                    alert.classList.contains('alert-info') ? 'info' : 'primary';
        
        const title = alert.querySelector('.alert-heading')?.textContent || 
                     (type === 'success' ? 'Éxito' :
                      type === 'error' ? 'Error' :
                      type === 'warning' ? 'Advertencia' :
                      type === 'info' ? 'Información' : 'Mensaje');
        
        const message = alert.textContent.replace(title, '').trim();
        
        customAlerts.show(type, title, message, 5000);
        
        // Ocultar la alerta original
        alert.style.display = 'none';
    });
};

// Función para validación de formularios
window.showFormValidation = (field, message, type = 'error') => {
    // Remover alertas anteriores del campo
    const existingAlert = field.parentElement.querySelector('.inline-alert');
    if (existingAlert) {
        existingAlert.remove();
    }

    // Crear nueva alerta
    const alert = document.createElement('div');
    alert.className = `inline-alert ${type}`;
    alert.innerHTML = `<i class="fas fa-exclamation-circle me-1"></i>${message}`;
    
    field.parentElement.appendChild(alert);
    
    // Resaltar campo con error
    field.classList.add('is-invalid');
    
    return alert;
};

// Función para limpiar validaciones
window.clearFormValidation = (field) => {
    const alert = field.parentElement.querySelector('.inline-alert');
    if (alert) {
        alert.remove();
    }
    field.classList.remove('is-invalid');
};

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar flash messages existentes
    showFlashMessages();
    
    // Configurar validación de formularios
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    showFormValidation(field, 'Este campo es obligatorio');
                    isValid = false;
                } else {
                    clearFormValidation(field);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showError('Error de Validación', 'Por favor, completa todos los campos requeridos.');
            }
        });
    });
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CustomAlerts;
} 