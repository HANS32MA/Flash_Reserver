/**
 * Sistema de Notificaciones en Tiempo Real para Flash Reserver
 * Maneja WebSockets, notificaciones push y notificaciones in-app
 */

class NotificationManager {
    constructor() {
        this.socket = null;
        this.notificationContainer = null;
        this.notificationCount = 0;
        this.notifications = [];
        this.isConnected = false;
        this.userId = null;
        this.isAdmin = false;
        
        this.init();
    }
    
    init() {
        this.setupNotificationContainer();
        this.setupWebSocket();
        this.setupServiceWorker();
        this.setupNotificationPermissions();
        this.loadStoredNotifications();
    }
    
    setupNotificationContainer() {
        // Crear contenedor de notificaciones si no existe
        if (!document.getElementById('notification-container')) {
            this.notificationContainer = document.createElement('div');
            this.notificationContainer.id = 'notification-container';
            this.notificationContainer.className = 'notification-container';
            document.body.appendChild(this.notificationContainer);
        } else {
            this.notificationContainer = document.getElementById('notification-container');
        }
        
        // Crear botón de notificaciones si no existe
        if (!document.getElementById('notification-btn')) {
            this.createNotificationButton();
        }
    }
    
    createNotificationButton() {
        const notificationBtn = document.createElement('div');
        notificationBtn.id = 'notification-btn';
        notificationBtn.className = 'notification-btn';
        notificationBtn.innerHTML = `
            <i class="fas fa-bell"></i>
            <span class="notification-badge" id="notification-badge">0</span>
        `;
        
        notificationBtn.addEventListener('click', () => this.toggleNotificationPanel());
        
        // Buscar un lugar apropiado para colocar el botón
        const header = document.querySelector('header') || document.querySelector('.navbar') || document.body;
        header.appendChild(notificationBtn);
    }
    
    setupWebSocket() {
        try {
            // Conectar al WebSocket
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('Conectado al servidor de notificaciones');
                this.isConnected = true;
                this.joinUserRoom();
            });
            
            this.socket.on('disconnect', () => {
                console.log('Desconectado del servidor de notificaciones');
                this.isConnected = false;
            });
            
            this.socket.on('new_notification', (data) => {
                this.handleNewNotification(data);
            });
            
            this.socket.on('admin_notification', (data) => {
                this.handleAdminNotification(data);
            });
            
            this.socket.on('broadcast_notification', (data) => {
                this.handleBroadcastNotification(data);
            });
            
            this.socket.on('error', (data) => {
                console.error('Error en WebSocket:', data.message);
                this.showErrorNotification(data.message);
            });
            
        } catch (error) {
            console.error('Error configurando WebSocket:', error);
        }
    }
    
    joinUserRoom() {
        if (this.userId && this.socket) {
            this.socket.emit('join_user_room', { user_id: this.userId });
            
            if (this.isAdmin) {
                this.socket.emit('join_admin_room', { 
                    user_id: this.userId, 
                    is_admin: true 
                });
            }
        }
    }
    
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/notification-sw.js')
                .then(registration => {
                    console.log('Service Worker registrado:', registration);
                })
                .catch(error => {
                    console.error('Error registrando Service Worker:', error);
                });
        }
    }
    
    async setupNotificationPermissions() {
        if ('Notification' in window) {
            if (Notification.permission === 'default') {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    console.log('Permisos de notificación concedidos');
                }
            }
        }
    }
    
    handleNewNotification(data) {
        console.log('Nueva notificación recibida:', data);
        
        // Agregar a la lista de notificaciones
        this.notifications.unshift({
            id: Date.now(),
            ...data,
            timestamp: data.timestamp || new Date().toISOString()
        });
        
        // Actualizar contador
        this.updateNotificationCount();
        
        // Mostrar notificación
        this.showNotification(data);
        
        // Guardar en localStorage
        this.saveNotifications();
        
        // Enviar notificación push si está permitido
        this.sendPushNotification(data);
    }
    
    handleAdminNotification(data) {
        if (this.isAdmin) {
            console.log('Notificación de administrador recibida:', data);
            this.handleNewNotification(data);
        }
    }
    
    handleBroadcastNotification(data) {
        console.log('Notificación broadcast recibida:', data);
        this.handleNewNotification(data);
    }
    
    showNotification(data) {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${data.type || 'info'}`;
        notification.innerHTML = `
            <div class="notification-header">
                <span class="notification-title">${data.title || 'Notificación'}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
            <div class="notification-body">
                <p>${data.message}</p>
                <small class="notification-time">${this.formatTime(data.timestamp)}</small>
            </div>
        `;
        
        // Agregar al contenedor
        this.notificationContainer.appendChild(notification);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
        
        // Agregar clase de entrada
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
    }
    
    showErrorNotification(message) {
        this.showNotification({
            type: 'error',
            title: 'Error',
            message: message
        });
    }
    
    updateNotificationCount() {
        this.notificationCount = this.notifications.length;
        const badge = document.getElementById('notification-badge');
        if (badge) {
            badge.textContent = this.notificationCount;
            badge.style.display = this.notificationCount > 0 ? 'block' : 'none';
        }
    }
    
    toggleNotificationPanel() {
        const panel = document.getElementById('notification-panel');
        if (panel) {
            panel.classList.toggle('show');
        } else {
            this.createNotificationPanel();
        }
    }
    
    createNotificationPanel() {
        const panel = document.createElement('div');
        panel.id = 'notification-panel';
        panel.className = 'notification-panel';
        panel.innerHTML = `
            <div class="notification-panel-header">
                <h3>Notificaciones (${this.notificationCount})</h3>
                <button class="notification-panel-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
            <div class="notification-panel-body">
                ${this.renderNotificationList()}
            </div>
            <div class="notification-panel-footer">
                <button onclick="notificationManager.clearAllNotifications()">Limpiar Todo</button>
            </div>
        `;
        
        document.body.appendChild(panel);
        panel.classList.add('show');
    }
    
    renderNotificationList() {
        if (this.notifications.length === 0) {
            return '<p class="no-notifications">No hay notificaciones</p>';
        }
        
        return this.notifications.map(notif => `
            <div class="notification-item notification-item-${notif.type || 'info'}">
                <div class="notification-item-header">
                    <span class="notification-item-title">${notif.title || 'Notificación'}</span>
                    <small class="notification-item-time">${this.formatTime(notif.timestamp)}</small>
                </div>
                <div class="notification-item-body">
                    <p>${notif.message}</p>
                </div>
                <button class="notification-item-close" onclick="notificationManager.removeNotification(${notif.id})">&times;</button>
            </div>
        `).join('');
    }
    
    removeNotification(id) {
        this.notifications = this.notifications.filter(n => n.id !== id);
        this.updateNotificationCount();
        this.saveNotifications();
        this.refreshNotificationPanel();
    }
    
    clearAllNotifications() {
        this.notifications = [];
        this.updateNotificationCount();
        this.saveNotifications();
        this.refreshNotificationPanel();
    }
    
    refreshNotificationPanel() {
        const panel = document.getElementById('notification-panel');
        if (panel) {
            const body = panel.querySelector('.notification-panel-body');
            if (body) {
                body.innerHTML = this.renderNotificationList();
            }
        }
    }
    
    async sendPushNotification(data) {
        if ('Notification' in window && Notification.permission === 'granted') {
            try {
                const notification = new Notification(data.title || 'Flash Reserver', {
                    body: data.message,
                    icon: '/static/images/logo.png',
                    badge: '/static/images/favicon.png',
                    tag: 'flash-reserver-notification',
                    data: data
                });
                
                notification.onclick = () => {
                    window.focus();
                    notification.close();
                };
                
                // Auto-cerrar después de 5 segundos
                setTimeout(() => {
                    notification.close();
                }, 5000);
                
            } catch (error) {
                console.error('Error enviando notificación push:', error);
            }
        }
    }
    
    formatTime(timestamp) {
        if (!timestamp) return 'Ahora';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Hace un momento';
        if (diff < 3600000) return `Hace ${Math.floor(diff / 60000)} minutos`;
        if (diff < 86400000) return `Hace ${Math.floor(diff / 3600000)} horas`;
        
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    saveNotifications() {
        try {
            localStorage.setItem('flash-reserver-notifications', JSON.stringify(this.notifications));
        } catch (error) {
            console.error('Error guardando notificaciones:', error);
        }
    }
    
    loadStoredNotifications() {
        try {
            const stored = localStorage.getItem('flash-reserver-notifications');
            if (stored) {
                this.notifications = JSON.parse(stored);
                this.updateNotificationCount();
            }
        } catch (error) {
            console.error('Error cargando notificaciones:', error);
        }
    }
    
    setUserInfo(userId, isAdmin = false) {
        this.userId = userId;
        this.isAdmin = isAdmin;
        
        if (this.isConnected) {
            this.joinUserRoom();
        }
    }
    
    // Métodos para enviar notificaciones
    sendNotification(targetUserId, message, type = 'message') {
        if (this.socket && this.isConnected) {
            this.socket.emit('send_notification', {
                target_user_id: targetUserId,
                message: message,
                type: type,
                from_user: this.userId,
                timestamp: new Date().toISOString()
            });
        }
    }
}

// Inicializar el gestor de notificaciones
const notificationManager = new NotificationManager();

// Exportar para uso global
window.notificationManager = notificationManager;

// Configurar información del usuario cuando esté disponible
document.addEventListener('DOMContentLoaded', () => {
    // Intentar obtener información del usuario del DOM o de variables globales
    const userElement = document.querySelector('[data-user-id]');
    if (userElement) {
        const userId = userElement.dataset.userId;
        const isAdmin = userElement.dataset.isAdmin === 'true';
        notificationManager.setUserInfo(userId, isAdmin);
    }
    
    // También buscar en variables globales
    if (typeof window.currentUser !== 'undefined') {
        notificationManager.setUserInfo(
            window.currentUser.id,
            window.currentUser.is_admin || false
        );
    }
});

// Manejar eventos de página
window.addEventListener('beforeunload', () => {
    if (notificationManager.socket) {
        notificationManager.socket.disconnect();
    }
});
