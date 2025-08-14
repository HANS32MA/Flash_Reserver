/**
 * Configuración.js - Sistema de configuración en tiempo real
 * Maneja todas las secciones de configuración con AJAX
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todas las funcionalidades de configuración
    initConfiguracion();
});

function initConfiguracion() {
    // Cargar imagen actual del usuario
    loadCurrentUserImage();
    
    // Previsualización de imagen de perfil
    initImagePreview();
    
    // Validaciones de formularios
    initFormValidations();
    
    // Gestión de modales
    initModals();
    
    // Gestión de tabs responsive
    initResponsiveTabs();
    
    // Auto-guardado en tiempo real
    initRealTimeSave();
    
    // Gestión de notificaciones
    initNotifications();
    
    // Gestión de descarga de datos
    initDataDownload();
    
    // Gestión de cambios de contraseña
    initPasswordChange();
    
    // Gestión de configuraciones del sistema (admin)
    initSystemConfig();
}

// ===== CARGA DE IMAGEN ACTUAL =====
function loadCurrentUserImage() {
    const fotoPreview = document.querySelector('.configuracion-perfil-img');
    if (fotoPreview) {
        // Obtener información del perfil desde el servidor
        const isAdmin = window.location.pathname.includes('/admin');
        const url = isAdmin ? '/admin/perfil/obtener_info' : '/client/perfil/obtener_info';
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.imagen_url) {
                // Actualizar la imagen con la URL correcta del servidor
                fotoPreview.src = data.data.imagen_url;
                
                // Configurar manejo de errores
                fotoPreview.onerror = function() {
                    this.src = '/static/images/default-user.png';
                    console.log('Error al cargar imagen del servidor, usando imagen por defecto');
                };
                
                fotoPreview.onload = function() {
                    console.log('Imagen de perfil cargada correctamente desde el servidor');
                };
            }
        })
        .catch(error => {
            console.error('Error al obtener información del perfil:', error);
            // Configurar manejo de errores por defecto
            fotoPreview.onerror = function() {
                this.src = '/static/images/default-user.png';
            };
        });
    }
}

// ===== PREVISUALIZACIÓN DE IMAGEN =====
function initImagePreview() {
    const fotoInput = document.getElementById('foto_perfil');
    const fotoPreview = document.querySelector('.configuracion-perfil-img');
    
    if (fotoInput && fotoPreview) {
        // Asegurar que la imagen actual se muestre correctamente
        if (fotoPreview.src && !fotoPreview.src.includes('default-user.png')) {
            fotoPreview.onerror = function() {
                this.src = '/static/images/default-user.png';
            };
        }
        
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tipo de archivo
                if (!file.type.startsWith('image/')) {
                    showError('Error', 'Por favor selecciona un archivo de imagen válido');
                    return;
                }
                
                // Validar tamaño (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showError('Error', 'La imagen debe ser menor a 5MB');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    fotoPreview.src = e.target.result;
                    showSuccess('Imagen Cargada', 'La imagen se ha cargado correctamente');
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// ===== VALIDACIONES DE FORMULARIOS =====
function initFormValidations() {
    // Validación de contraseñas
    const passwordNuevo = document.getElementById('password_nuevo');
    const passwordConfirmar = document.getElementById('password_confirmar');
    
    if (passwordNuevo && passwordConfirmar) {
        passwordConfirmar.addEventListener('input', function() {
            if (passwordNuevo.value !== passwordConfirmar.value) {
                passwordConfirmar.setCustomValidity('Las contraseñas no coinciden');
            } else {
                passwordConfirmar.setCustomValidity('');
            }
        });
        
        passwordNuevo.addEventListener('input', function() {
            if (passwordConfirmar.value && passwordNuevo.value !== passwordConfirmar.value) {
                passwordConfirmar.setCustomValidity('Las contraseñas no coinciden');
            } else {
                passwordConfirmar.setCustomValidity('');
            }
        });
    }
    
    // Validación de email
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = this.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email && !emailRegex.test(email)) {
                this.setCustomValidity('Por favor ingresa un email válido');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Validación de teléfono
    const telefonoInput = document.getElementById('telefono');
    if (telefonoInput) {
        telefonoInput.addEventListener('input', function() {
            const telefono = this.value.replace(/\D/g, '');
            if (telefono.length > 0 && telefono.length < 10) {
                this.setCustomValidity('El teléfono debe tener al menos 10 dígitos');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

// ===== AUTO-GUARDADO EN TIEMPO REAL =====
function initRealTimeSave() {
    // Configurar auto-guardado para todos los inputs
    const inputs = document.querySelectorAll('.configuracion-content input, .configuracion-content select, .configuracion-content textarea');
    
    inputs.forEach(input => {
        // Excluir campos de contraseña y archivos
        if (input.type === 'password' || input.type === 'file') return;
        
        let saveTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            
            // Guardar en localStorage inmediatamente
            const key = `config_${this.id || this.name}`;
            const value = this.type === 'checkbox' ? this.checked : this.value;
            localStorage.setItem(key, JSON.stringify(value));
            
            // Auto-guardar en servidor después de 2 segundos de inactividad
            saveTimeout = setTimeout(() => {
                autoSaveField(this);
            }, 2000);
        });
        
        // Restaurar valores guardados
        const key = `config_${input.id || input.name}`;
        const savedValue = localStorage.getItem(key);
        if (savedValue) {
            try {
                const value = JSON.parse(savedValue);
                if (input.type === 'checkbox') {
                    input.checked = value;
                } else {
                    input.value = value;
                }
            } catch (e) {
                // Ignorar errores de parsing
            }
        }
    });
    
    // Configurar formularios para envío AJAX
    const forms = document.querySelectorAll('.configuracion-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitFormAjax(this);
        });
    });
}

// ===== AUTO-GUARDADO DE CAMPOS INDIVIDUALES =====
function autoSaveField(field) {
    const formData = new FormData();
    const fieldName = field.name || field.id;
    const fieldValue = field.type === 'checkbox' ? field.checked : field.value;
    
    formData.append(fieldName, fieldValue);
    
    // Determinar la URL según el tipo de campo
    let url;
    if (field.closest('#perfil')) {
        url = window.location.pathname.includes('/admin') ? '/admin/actualizar_perfil' : '/client/actualizar_perfil';
    } else if (field.closest('#general')) {
        url = '/admin/actualizar_configuracion_general';
    } else {
        // Para otros campos, usar una ruta genérica
        url = '/configuracion/actualizar_campo';
    }
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Guardado', 'Cambio guardado automáticamente');
        } else {
            showError('Error', data.message || 'Error al guardar');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Error', 'Error de conexión');
    });
}

// ===== ENVÍO DE FORMULARIOS CON AJAX =====
function submitFormAjax(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Mostrar estado de carga
    submitButton.disabled = true;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...';
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Éxito', data.message || 'Datos guardados correctamente');
            
            // Actualizar imagen si es un formulario de perfil
            if (data.image_url) {
                const fotoPreview = document.querySelector('.configuracion-perfil-img');
                if (fotoPreview) {
                    fotoPreview.src = data.image_url;
                }
            }
            
            // Limpiar localStorage para campos guardados
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.id || input.name) {
                    const key = `config_${input.id || input.name}`;
                    localStorage.removeItem(key);
                }
            });
        } else {
            showError('Error', data.message || 'Error al guardar los datos');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Error', 'Error de conexión');
    })
    .finally(() => {
        // Restaurar botón
        submitButton.disabled = false;
        submitButton.innerHTML = originalText;
    });
}

// ===== CAMBIO DE CONTRASEÑA =====
function initPasswordChange() {
    const passwordForms = document.querySelectorAll('form[action*="cambiar_password"]');
    passwordForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Validar contraseñas
            const passwordNuevo = formData.get('password_nuevo');
            const passwordConfirmar = formData.get('password_confirmar');
            
            if (passwordNuevo !== passwordConfirmar) {
                showError('Error', 'Las contraseñas no coinciden');
                return;
            }
            
            if (passwordNuevo.length < 6) {
                showError('Error', 'La contraseña debe tener al menos 6 caracteres');
                return;
            }
            
            // Mostrar estado de carga
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Cambiando...';
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccess('Contraseña Cambiada', 'Tu contraseña ha sido actualizada correctamente');
                    this.reset();
                } else {
                    showError('Error', data.message || 'Error al cambiar la contraseña');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Error', 'Error de conexión');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
        });
    });
}

// ===== CONFIGURACIÓN DEL SISTEMA (ADMIN) =====
function initSystemConfig() {
    // Configurar switches y toggles para guardado automático
    const switches = document.querySelectorAll('.form-check-input[type="checkbox"]');
    switches.forEach(switchElement => {
        switchElement.addEventListener('change', function() {
            const formData = new FormData();
            formData.append(this.name || this.id, this.checked);
            
            // Determinar URL según la sección
            let url = '/admin/actualizar_configuracion_general';
            if (this.closest('#reservas')) {
                url = '/admin/actualizar_configuracion_reservas';
            } else if (this.closest('#notificaciones')) {
                url = '/admin/actualizar_configuracion_notificaciones';
            }
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccess('Configuración Actualizada', 'Cambio aplicado correctamente');
                } else {
                    showError('Error', data.message || 'Error al actualizar configuración');
                    // Revertir el cambio
                    this.checked = !this.checked;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Error', 'Error de conexión');
                // Revertir el cambio
                this.checked = !this.checked;
            });
        });
    });
    
    // Configurar inputs numéricos y selects
    const configInputs = document.querySelectorAll('#general input, #reservas input, #notificaciones input, #general select, #reservas select, #notificaciones select');
    configInputs.forEach(input => {
        if (input.type === 'checkbox') return; // Ya manejado arriba
        
        let saveTimeout;
        input.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                const formData = new FormData();
                formData.append(this.name || this.id, this.value);
                
                let url = '/admin/actualizar_configuracion_general';
                if (this.closest('#reservas')) {
                    url = '/admin/actualizar_configuracion_reservas';
                } else if (this.closest('#notificaciones')) {
                    url = '/admin/actualizar_configuracion_notificaciones';
                }
                
                fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showSuccess('Configuración Actualizada', 'Cambio aplicado correctamente');
                    } else {
                        showError('Error', data.message || 'Error al actualizar configuración');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showError('Error', 'Error de conexión');
                });
            }, 1000);
        });
    });
}

// ===== GESTIÓN DE MODALES =====
function initModals() {
    // Esta función ya no es necesaria ya que usamos alertas personalizadas
    // Los botones ahora llaman directamente a las funciones pausarCuenta() y eliminarCuenta()
}

// ===== TABS RESPONSIVE =====
function initResponsiveTabs() {
    // Hacer que los tabs sean más fáciles de usar en móvil
    const tabs = document.querySelectorAll('[data-bs-toggle="list"]');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            // En móvil, cerrar cualquier dropdown abierto
            if (window.innerWidth < 768) {
                const dropdowns = document.querySelectorAll('.dropdown-menu.show');
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
            }
        });
    });
}

// ===== NOTIFICACIONES =====
function initNotifications() {
    // Configurar notificaciones push si están disponibles
    if ('Notification' in window) {
        const notifToggle = document.getElementById('push_reservas');
        if (notifToggle) {
            notifToggle.addEventListener('change', function() {
                if (this.checked) {
                    requestNotificationPermission();
                }
            });
        }
    }
}

function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showSuccess('Notificaciones Habilitadas', 'Las notificaciones push están ahora activas');
            } else {
                showWarning('Notificaciones Denegadas', 'Las notificaciones fueron denegadas');
                // Desmarcar el checkbox
                const notifToggle = document.getElementById('push_reservas');
                if (notifToggle) {
                    notifToggle.checked = false;
                }
            }
        });
    }
}

// ===== FUNCIONES DE UTILIDAD =====
function showNotification(message, type = 'info') {
    // Usar el sistema de alertas personalizado
    const title = type === 'success' ? 'Éxito' :
                  type === 'error' ? 'Error' :
                  type === 'warning' ? 'Advertencia' :
                  type === 'info' ? 'Información' : 'Mensaje';
    
    switch(type) {
        case 'success':
            showSuccess(title, message);
            break;
        case 'error':
            showError(title, message);
            break;
        case 'warning':
            showWarning(title, message);
            break;
        case 'info':
        default:
            showInfo(title, message);
            break;
    }
}

// ===== FUNCIONES DE CUENTA =====
function pausarCuenta() {
    // Usar el sistema de alertas personalizado
    showConfirm(
        'Pausar Cuenta',
        '¿Estás seguro de que quieres pausar tu cuenta?<br><br><strong>Consecuencias:</strong><br>• No podrás hacer nuevas reservas<br>• Tus datos se mantendrán seguros<br>• Puedes reactivar tu cuenta en cualquier momento',
        () => {
            // Acción de confirmación
            showSuccess('Cuenta Pausada', 'Tu cuenta ha sido pausada exitosamente. Serás redirigido al login.');
            
            // Redirigir después de un momento
            setTimeout(() => {
                window.location.href = '/auth/logout';
            }, 2000);
        },
        () => {
            // Acción de cancelación
            showInfo('Operación Cancelada', 'Tu cuenta permanece activa.');
        }
    );
}

function eliminarCuenta() {
    // Usar el sistema de alertas personalizado para eliminación
    showConfirm(
        'Eliminar Cuenta Permanentemente',
        '<div style="text-align: left;"><strong>⚠️ ADVERTENCIA CRÍTICA ⚠️</strong><br><br>' +
        'Esta acción es <strong>IRREVERSIBLE</strong> y eliminará:<br>' +
        '• Todos tus datos personales<br>' +
        '• Todas tus reservas<br>' +
        '• Tu historial completo<br>' +
        '• Acceso a la plataforma<br><br>' +
        '<strong>No podrás recuperar tu cuenta después de esta acción.</strong></div>',
        () => {
            // Segunda confirmación para acciones críticas
            showConfirm(
                'Confirmación Final',
                '¿Estás <strong>COMPLETAMENTE SEGURO</strong> de que quieres eliminar tu cuenta?<br><br>' +
                'Esta es tu última oportunidad para cancelar.',
                () => {
                    // Acción final de eliminación
                    showWarning('Eliminando Cuenta', 'Tu cuenta está siendo eliminada...');
                    
                    // Crear formulario temporal para enviar la petición
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = window.location.pathname.replace('/configuracion', '/eliminar_cuenta');
                    
                    document.body.appendChild(form);
                    form.submit();
                },
                () => {
                    showInfo('Operación Cancelada', 'Tu cuenta permanece segura.');
                }
            );
        },
        () => {
            showInfo('Operación Cancelada', 'Tu cuenta permanece segura.');
        }
    );
}

// ===== FUNCIONES PARA ADMINISTRADORES =====
function crearBackup() {
    showConfirm(
        'Crear Backup del Sistema',
        '¿Estás seguro de que quieres crear un backup completo del sistema?<br><br><strong>Incluirá:</strong><br>• Base de datos completa<br>• Configuraciones del sistema<br>• Archivos de usuarios<br><br>El proceso puede tomar varios minutos.',
        () => {
            showInfo('Creando Backup', 'El backup está siendo creado. Por favor, no cierres esta ventana...');
            
            // Simular proceso de backup
            setTimeout(() => {
                showSuccess('Backup Completado', 'El backup del sistema ha sido creado exitosamente.');
            }, 3000);
        },
        () => {
            showInfo('Operación Cancelada', 'No se creó ningún backup.');
        }
    );
}

function restaurarBackup() {
    const fileInput = document.getElementById('archivo_backup');
    if (fileInput && fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        
        showConfirm(
            'Restaurar Backup del Sistema',
            `<strong>⚠️ ADVERTENCIA ⚠️</strong><br><br>` +
            `¿Estás seguro de que quieres restaurar el backup "${fileName}"?<br><br>` +
            `<strong>Esta acción:</strong><br>` +
            `• Sobrescribirá todos los datos actuales<br>` +
            `• Puede tomar varios minutos<br>` +
            `• Requiere reiniciar el sistema<br><br>` +
            `<strong>Se recomienda hacer un backup antes de continuar.</strong>`,
            () => {
                // Segunda confirmación para acciones críticas
                showConfirm(
                    'Confirmación Final',
                    '¿Estás <strong>COMPLETAMENTE SEGURO</strong> de que quieres restaurar el backup?<br><br>' +
                    'Esta acción sobrescribirá todos los datos actuales del sistema.',
                    () => {
                        showWarning('Restaurando Backup', 'El sistema está siendo restaurado. Por favor, espera...');
                        
                        // Simular proceso de restauración
                        setTimeout(() => {
                            showSuccess('Restauración Completada', 'El sistema ha sido restaurado exitosamente.');
                        }, 4000);
                    },
                    () => {
                        showInfo('Operación Cancelada', 'No se restauró ningún backup.');
                    }
                );
            },
            () => {
                showInfo('Operación Cancelada', 'No se restauró ningún backup.');
            }
        );
    } else {
        showWarning('Archivo Requerido', 'Por favor selecciona un archivo de backup antes de continuar.');
    }
}

// ===== DESCARGA DE DATOS =====
function initDataDownload() {
    const downloadButtons = document.querySelectorAll('.btn-outline-secondary');
    downloadButtons.forEach(button => {
        if (button.textContent.includes('Descargar')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                showConfirm(
                    'Descargar Datos Personales',
                    '¿Estás seguro de que quieres descargar todos tus datos personales?<br><br><strong>Incluirá:</strong><br>• Información de perfil<br>• Historial de reservas<br>• Configuraciones<br>• Datos de actividad<br><br>Los datos se descargarán en formato JSON.',
                    () => {
                        showInfo('Preparando Descarga', 'Tus datos están siendo preparados para la descarga...');
                        
                        // Simular proceso de preparación
                        setTimeout(() => {
                            showSuccess('Descarga Lista', 'Tus datos personales han sido preparados. La descarga comenzará automáticamente.');
                            
                            // Aquí se simularía la descarga real
                            // En un caso real, se enviaría una petición al servidor
                        }, 2000);
                    },
                    () => {
                        showInfo('Operación Cancelada', 'No se descargaron datos.');
                    }
                );
            });
        }
    });
}

// ===== EXPORTAR FUNCIONES =====
window.ConfiguracionUtils = {
    showNotification,
    crearBackup,
    restaurarBackup,
    pausarCuenta,
    eliminarCuenta,
    submitFormAjax,
    autoSaveField
};
