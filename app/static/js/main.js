// Funciones de utilidad
window.showAlert = function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
    const container = document.querySelector('.container') || document.body;
            container.insertBefore(alertDiv, container.firstChild);
            
            setTimeout(() => {
                    alertDiv.remove();
            }, 5000);
    };

    // Función para formatear moneda
    window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('es-CO', {
            style: 'currency',
        currency: 'COP'
        }).format(amount);
    };

// Función para manejar errores de fetch
window.handleFetchError = function(response, errorCallback) {
    if (!response.ok) {
        if (response.status === 401) {
            window.location.href = '/auth/login';
            } else {
            errorCallback({ error: `Error ${response.status}: ${response.statusText}` });
        }
    } else {
        return response.json();
    }
};

// Función para manejar errores de conexión
window.handleConnectionError = function(error, errorCallback) {
    console.error('Error de conexión:', error);
            if (errorCallback) errorCallback({ error: 'Error de conexión' });
    };

// Función para obtener horarios disponibles
window.getHorariosDisponibles = function(canchaId, fecha, successCallback, errorCallback) {
    try {
        const url = `/client/api/horarios-disponibles/${canchaId}?fecha=${fecha}`;
        
        fetch(url)
            .then(response => handleFetchError(response, errorCallback))
            .then(data => {
                if (data && successCallback) {
                    successCallback(data);
                }
            })
            .catch(error => handleConnectionError(error, errorCallback));
        } catch (error) {
        console.error('Error en getHorariosDisponibles:', error);
    }
};

// Función para generar resumen de reserva
window.generateReservationSummary = function(reserva) {
    const { cancha, fecha, horaInicio, duracion, precioTotal } = reserva;
    
    return `
        <div class="reservation-summary">
            <h5>Resumen de Reserva</h5>
            <p><strong>Cancha:</strong> ${cancha}</p>
                <p><strong>Fecha:</strong> ${formatDate(fecha)}</p>
                <p><strong>Horario:</strong> ${horaInicio} - ${calculateEndTime(horaInicio, duracion)}</p>
                <p><strong>Duración:</strong> ${duracion} hora(s)</p>
                <p><strong>Precio total:</strong> ${formatCurrency(precioTotal)}</p>
        </div>
    `;
};

// Función para descargar archivos
window.downloadFile = function(content, filename, mimeType = 'text/plain') {
    try {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error descargando archivo:', error);
    }
};

// Función para exportar a CSV
window.exportToCSV = function(data, filename) {
    if (!data || data.length === 0) return;
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
        ].join('\n');
        
    downloadFile(csvContent, filename, 'text/csv');
    };

    // Función para compartir en redes sociales
window.shareOnSocialMedia = function(url, text) {
        const shareUrls = {
            facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
            twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`,
            whatsapp: `https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`
        };
        
    return shareUrls;
};

// Función para abrir ventana de compartir
window.openShareWindow = function(url, platform) {
    const shareUrls = shareOnSocialMedia(url, '¡Mira esta cancha!');
        if (shareUrls[platform]) {
            window.open(shareUrls[platform], '_blank', 'width=600,height=400');
        }
    };

// Funciones para el sistema de notificaciones
window.actualizarContadorNotificaciones = function() {
    const notificationCount = document.getElementById('notificationCount');
    if (notificationCount) {
        if (window.notificationCount > 0) {
            notificationCount.textContent = window.notificationCount;
            notificationCount.style.display = 'inline-block';
        } else {
            notificationCount.style.display = 'none';
        }
    }
};

// Función para marcar conversación como leída
window.marcarConversacionLeida = function(usuarioId) {
    fetch('/admin/marcar-conversacion-leida', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ usuario_id: usuarioId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.notificationCount = Math.max(0, window.notificationCount - 1);
            window.actualizarContadorNotificaciones();
        }
    })
    .catch(error => {
        console.error('Error marcando como leída:', error);
    });
};

// Función para marcar todas las notificaciones como leídas
window.marcarTodasComoLeidas = function() {
    fetch('/admin/marcar-notificaciones-leidas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.notificationCount = 0;
            window.actualizarContadorNotificaciones();
            window.cargarNotificaciones();
            showAlert('success', 'Éxito', 'Todas las notificaciones marcadas como leídas');
    } else {
            showAlert('error', 'Error', 'Error al marcar como leídas: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error marcando todas como leídas:', error);
        showAlert('error', 'Error', 'Error al marcar como leídas');
    });
};

// Función para mostrar detalles del mensaje
window.mostrarDetalleMensaje = function(mensajeId) {
    const selectedItem = document.querySelector(`#mensajesList .list-group-item[data-id="${mensajeId}"]`);
    if (selectedItem) {
        document.querySelectorAll('#mensajesList .list-group-item').forEach(item => {
            item.classList.remove('active');
        });
        selectedItem.classList.add('active');
    }
    
    fetch(`/admin/mensaje/${mensajeId}`)
                .then(response => response.json())
                .then(data => {
            if (data.success) {
                const mensaje = data.mensaje;
                const detailContainer = document.getElementById('mensajeDetalle');
                
                detailContainer.innerHTML = `
                    <div class="mensaje-detalle">
                            <h6 class="text-primary">${mensaje.asunto}</h6>
                            <small class="text-muted">De: ${mensaje.usuario_nombre} - ${mensaje.fecha}</small>
                        <hr>
                            <p class="mb-0">${mensaje.mensaje}</p>
                        ${mensaje.respuesta ? `
                        <hr>
                        <h6 class="text-success">Respuesta:</h6>
                            <small class="text-muted d-block mb-2">${mensaje.fecha_respuesta}</small>
                            <p class="mb-0">${mensaje.respuesta}</p>
                        ` : ''}
                        ${!mensaje.respuesta ? `
                        <hr>
                            <button class="btn btn-responder" onclick="responderMensaje(${mensaje.id})">
                            <i class="fas fa-reply"></i> Responder
                            </button>
                        ` : ''}
                    </div>
                `;
            }
                })
                .catch(error => {
            console.error('Error cargando detalle del mensaje:', error);
        });
};

// Función para responder mensaje
window.responderMensaje = function(notificationId) {
    const detailContainer = document.getElementById('mensajeDetalle');
    detailContainer.innerHTML = `
        <div class="respuesta-form">
            <h6>Responder Mensaje</h6>
                        <div class="mb-3">
                <textarea class="form-control" id="respuestaText" rows="4" placeholder="Escribe tu respuesta..."></textarea>
                        </div>
            <div class="d-flex gap-2">
                <button type="button" class="btn btn-secondary" onclick="mostrarDetalleMensaje(${notificationId})">
                    Cancelar
                </button>
                        <button type="button" class="btn btn-primary" onclick="enviarRespuesta(${notificationId})">
                    <i class="fas fa-paper-plane"></i> Enviar Respuesta
                        </button>
            </div>
        </div>
    `;
};

// Función para enviar respuesta
    window.enviarRespuesta = function(notificationId) {
        const respuesta = document.getElementById('respuestaText').value.trim();
        
        if (!respuesta) {
        showAlert('warning', 'Advertencia', 'Por favor escribe una respuesta');
            return;
        }
        
            fetch('/admin/responder-mensaje', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    notification_id: notificationId,
                respuesta: respuesta
            })
        })
    .then(response => response.json())
            .then(data => {
                if (data.success) {
            showAlert('success', 'Éxito', 'Respuesta enviada correctamente');
            window.actualizarContadorNotificaciones();
            cargarNotificaciones();
                } else {
            showAlert('error', 'Error', 'Error al enviar respuesta: ' + data.error);
                }
            })
            .catch(error => {
        console.error('Error enviando respuesta:', error);
        showAlert('error', 'Error', 'Error al enviar respuesta');
        });
    };

// Función para cargar notificaciones
window.cargarNotificaciones = function() {
    const notificationCount = document.getElementById('notificationCount');
    
    if (!notificationCount || !document.body.classList.contains('admin-page')) {
        return;
    }
    
    fetch('/admin/notificaciones')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.notificationCount = data.unread_count || 0;
                window.actualizarContadorNotificaciones();
                window.mostrarNotificaciones(data.notifications || []);
            }
        })
        .catch((error) => {
            console.error('Error cargando notificaciones:', error);
        });
    };

// Función para mostrar notificaciones
window.mostrarNotificaciones = function(notifications) {
    const mensajesList = document.getElementById('mensajesList');
    if (!mensajesList) return;
    
    if (notifications.length === 0) {
        mensajesList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-inbox fa-3x mb-3"></i>
                <p>No hay mensajes nuevos</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    notifications.forEach(notification => {
        const isUnread = !notification.leido;
        const statusClass = notification.respuesta ? 'text-success' : (isUnread ? 'text-primary' : 'text-muted');
        const statusIcon = notification.respuesta ? 'fas fa-check-circle' : (isUnread ? 'fas fa-envelope' : 'fas fa-envelope-open');
        
        html += `
            <div class="list-group-item list-group-item-action ${isUnread ? 'active' : ''}" 
                 data-id="${notification.id}" 
                 onclick="mostrarConversacion(${notification.usuario_id}, '${notification.usuario_nombre}')">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1 ${statusClass}">
                            <i class="${statusIcon} me-2"></i>
                            ${notification.usuario_nombre}
                        </h6>
                        <p class="mb-1 small">${notification.asunto}</p>
                        <small class="text-muted">${notification.fecha}</small>
                    </div>
                    ${notification.respuesta ? '<span class="badge bg-success">CONFIRMADA</span>' : ''}
                </div>
            </div>
        `;
    });
    
    mensajesList.innerHTML = html;
};

// Función para mostrar conversación completa
window.mostrarConversacion = function(usuarioId, usuarioNombre) {
    // Limpiar intervalo anterior si existe
    if (window.chatInterval) {
        clearInterval(window.chatInterval);
    }
    
    // Marcar el mensaje como leído
    if (typeof marcarConversacionLeida === 'function') {
        marcarConversacionLeida(usuarioId);
    }
    
    // Actualizar la interfaz para mostrar el chat
    const detailContainer = document.getElementById('mensajeDetalle');
    
    if (detailContainer) {
        // Obtener información del usuario para la foto de perfil
        fetch(`/admin/conversacion/${usuarioId}`)
    .then(response => response.json())
    .then(data => {
                if (data.success && data.conversacion.length > 0) {
                    const mensaje = data.conversacion[0];
                    const fotoPerfil = mensaje.foto_perfil || '/static/images/default-user.png';
                    
                    detailContainer.innerHTML = `
                        <div class="chat-container">
                            <div class="chat-header">
                                <img src="${fotoPerfil}" alt="Avatar" class="user-avatar">
                                <h6>${usuarioNombre}</h6>
                            </div>
                            <div class="chat-messages" id="chatMessages-${usuarioId}">
                                <div class="text-center text-muted py-3">
                                    <i class="fas fa-spinner fa-spin"></i> Cargando mensajes...
                                </div>
                            </div>
                            <div class="chat-input-container">
                                <div class="input-group">
                                    <input type="text" 
                                           class="form-control" 
                                           id="chatInput-${usuarioId}" 
                                           placeholder="Escribe tu respuesta..."
                                           onkeypress="enviarRespuestaChat(event, ${usuarioId})">
                                    <button class="btn btn-primary" onclick="enviarRespuestaChatBtn(${usuarioId})">
                                        <i class="fas fa-paper-plane"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // Cargar mensajes iniciales
                    cargarMensajesChat(usuarioId);
                    
                    // Actualización automática deshabilitada temporalmente
                    // window.chatInterval = setInterval(() => {
                    //     cargarMensajesChat(usuarioId);
                    // }, 5000);
                    
                    // Guardar el usuarioId actual
                    window.currentChatUserId = usuarioId;
        }
    })
    .catch(error => {
                console.error('Error cargando información del usuario:', error);
                // Fallback sin foto de perfil
                detailContainer.innerHTML = `
                    <div class="chat-container">
                        <div class="chat-header">
                            <img src="/static/images/default-user.png" alt="Avatar" class="user-avatar">
                            <h6>${usuarioNombre}</h6>
                        </div>
                        <div class="chat-messages" id="chatMessages-${usuarioId}">
                            <div class="text-center text-muted py-3">
                                <i class="fas fa-spinner fa-spin"></i> Cargando mensajes...
                            </div>
                        </div>
                        <div class="chat-input-container">
                            <div class="input-group">
                                <input type="text" 
                                       class="form-control" 
                                       id="chatInput-${usuarioId}" 
                                       placeholder="Escribe tu respuesta..."
                                       onkeypress="enviarRespuestaChat(event, ${usuarioId})">
                                <button class="btn btn-primary" onclick="enviarRespuestaChatBtn(${usuarioId})">
                                    <i class="fas fa-paper-plane"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                
                // Cargar mensajes iniciales
                cargarMensajesChat(usuarioId);
                
                // Actualización automática deshabilitada temporalmente
                // window.chatInterval = setInterval(() => {
                //     cargarMensajesChat(usuarioId);
                // }, 5000);
                
                // Guardar el usuarioId actual
                window.currentChatUserId = usuarioId;
            });
        }
    };

// Función para cargar mensajes del chat
function cargarMensajesChat(usuarioId) {
    fetch(`/admin/conversacion/${usuarioId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const chatContainer = document.getElementById(`chatMessages-${usuarioId}`);
                if (chatContainer) {
                    let html = '';
                    
                    data.conversacion.forEach(mensaje => {
                        const mensajeClass = mensaje.respuesta ? 'admin-message' : 'user-message';
                        const icono = mensaje.respuesta ? 'fas fa-headset' : 'fas fa-user';
                        const nombre = mensaje.respuesta ? 'Admin' : 'Usuario';
                        const tiempo = mensaje.fecha_respuesta || mensaje.fecha;
                        
                        html += `
                            <div class="message ${mensajeClass}">
                                <div class="message-header">
                                    <i class="${icono} me-2"></i>
                                    <strong>${nombre}</strong>
                                    <small class="text-muted ms-2">${tiempo}</small>
                                </div>
                                <div class="message-content">
                                    <p>${mensaje.respuesta || mensaje.mensaje}</p>
                                </div>
                            </div>
                        `;
                    });
                    
                    chatContainer.innerHTML = html;
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
        })
        .catch(error => {
            console.error('Error cargando mensajes:', error);
        });
}

// Función para enviar respuesta desde el chat
window.enviarRespuestaChat = function(event, usuarioId) {
    if (event.key === 'Enter') {
        enviarRespuestaChatBtn(usuarioId);
    }
};

window.enviarRespuestaChatBtn = function(usuarioId) {
    const input = document.getElementById(`chatInput-${usuarioId}`);
    const respuesta = input.value.trim();
    
    if (respuesta && !window.enviandoRespuesta) {
        window.enviandoRespuesta = true;
        
        // Mostrar mensaje inmediatamente en el chat
        const chatContainer = document.getElementById(`chatMessages-${usuarioId}`);
        if (chatContainer) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message admin-message';
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-headset me-2"></i>
                    <strong>Admin</strong>
                    <small class="text-muted ms-2">Ahora</small>
                </div>
                <div class="message-content">
                    <p>${respuesta}</p>
                </div>
            `;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Limpiar input
        input.value = '';
        
        // Enviar al servidor
        fetch('/admin/responder-mensaje', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                notification_id: usuarioId,
                respuesta: respuesta
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.actualizarContadorNotificaciones();
                cargarNotificaciones();
            } else {
                console.error('Error al enviar respuesta:', data.error);
            }
        })
        .catch(error => {
            console.error('Error enviando respuesta:', error);
        })
        .finally(() => {
            window.enviandoRespuesta = false;
        });
    }
};

// Inicialización automática de notificaciones para administradores
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en una página de administrador
    if (document.body.classList.contains('admin-page') || 
        window.location.pathname.includes('/admin/')) {
        
        // Cargar notificaciones al cargar la página
        setTimeout(() => {
            if (typeof window.cargarNotificaciones === 'function') {
                window.cargarNotificaciones();
            }
        }, 1000);
        
        // Actualizar notificaciones cada 30 segundos
        setInterval(() => {
            if (typeof window.cargarNotificaciones === 'function') {
                window.cargarNotificaciones();
            }
        }, 30000);
        
        // Limpiar intervalo del chat cuando se cierre el modal
        const notificationModal = document.getElementById('notificationModal');
        if (notificationModal) {
            // Cargar notificaciones cuando se abra el modal
            notificationModal.addEventListener('shown.bs.modal', function() {
                if (typeof window.cargarNotificaciones === 'function') {
                    window.cargarNotificaciones();
                }
            });
            notificationModal.addEventListener('hidden.bs.modal', function() {
                if (window.chatInterval) {
                    clearInterval(window.chatInterval);
                    window.chatInterval = null;
                }
                // Limpiar el panel de chat
                const detailContainer = document.getElementById('mensajeDetalle');
                if (detailContainer) {
                    detailContainer.innerHTML = `
                        <div class="text-center text-muted">
                            <i class="fas fa-envelope-open fa-3x mb-3"></i>
                            <p>Selecciona un mensaje para ver su contenido</p>
                        </div>
                    `;
                }
            });
        }
    }
});

// Funciones para el botón flotante de ayuda y chat
document.addEventListener('DOMContentLoaded', function() {
    // Botón flotante de ayuda
    const floatingHelpBtn = document.getElementById('floatingHelpBtn');
    if (floatingHelpBtn) {
        floatingHelpBtn.addEventListener('click', function() {
            const modal = new bootstrap.Modal(document.getElementById('floatingHelpModal'));
            modal.show();
        });
    }

    // Funciones del chat - ULTRA SIMPLES
    window.abrirChat = function() {
        const modal = document.getElementById('floatingHelpModal');
        const chat = document.getElementById('chatWidget');
        const input = document.getElementById('chatInput');
        
        if (modal) modal.style.display = 'none';
        if (chat) chat.style.display = 'flex';
        if (input) input.focus();
        
        try {
            bootstrap.Modal.getInstance(document.getElementById('floatingHelpModal')).hide();
        } catch (e) {
            // Ignorar errores
        }
    };

    window.cerrarChat = function() {
        document.getElementById('chatWidget').style.display = 'none';
        document.getElementById('floatingHelpBtn').style.display = 'block';
    };

    window.minimizarChat = function() {
        document.getElementById('chatWidget').style.display = 'none';
        document.getElementById('floatingHelpBtn').style.display = 'block';
    };

    window.enviarMensajeChat = function(event) {
        if (event.key === 'Enter') {
            enviarMensajeChatBtn();
        }
    };

    // SISTEMA DE CHAT ULTRA SIMPLE - SIN BUCLES
    window.enviarMensajeChatBtn = function() {
        const input = document.getElementById('chatInput');
        const mensaje = input.value.trim();
        
        if (mensaje && !window.enviandoMensaje) {
            window.enviandoMensaje = true;
            
            // Solo mostrar mensaje en el chat
            const chatBody = document.getElementById('chatBody');
            if (chatBody) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <p>${mensaje}</p>
                        <small class="message-time">${new Date().toLocaleTimeString()}</small>
                    </div>
                `;
                chatBody.appendChild(messageDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            }
            
            // Limpiar input
            input.value = '';
            
            // Enviar al servidor de forma completamente aislada
            setTimeout(() => {
                fetch('/client/chat/mensaje', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mensaje: mensaje})
                })
                .finally(() => {
                    window.enviandoMensaje = false;
                });
            }, 100);
        }
    };
});

// Función para cambiar tema oscuro
window.setDarkMode = function(enabled) {
    const root = document.documentElement;
    const body = document.body;
    if (enabled) {
        root.classList.add('dark-mode');
        if (body) body.classList.add('dark-mode');
        localStorage.setItem('darkMode', '1');
        const themeIcon = document.getElementById('theme-icon');
        if (themeIcon) {
            themeIcon.className = 'fas fa-sun me-2';
        }
        const themeText = document.getElementById('theme-text');
        if (themeText) themeText.textContent = 'Tema Claro';
    } else {
        root.classList.remove('dark-mode');
        if (body) body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', '0');
        const themeIcon = document.getElementById('theme-icon');
        if (themeIcon) {
            themeIcon.className = 'fas fa-moon me-2';
        }
        const themeText = document.getElementById('theme-text');
        if (themeText) themeText.textContent = 'Tema Oscuro';
    }
};

// Inicializar tema oscuro
document.addEventListener('DOMContentLoaded', function() {
    const darkModeBtn = document.getElementById('btn-darkmode');
    
    if (darkModeBtn) {
        darkModeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const isDark = document.body.classList.contains('dark-mode');
            window.setDarkMode(!isDark);
        });
    }
    
    // Aplicar preferencia al cargar sin parpadeo
    const prefersDark = localStorage.getItem('darkMode') === '1';
    window.setDarkMode(prefersDark);
    

});



