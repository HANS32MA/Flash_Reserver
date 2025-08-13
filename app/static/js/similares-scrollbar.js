// Funcionalidad para la barra de navegación personalizada de canchas similares
document.addEventListener('DOMContentLoaded', function() {
    const similaresContainer = document.getElementById('similares-container');
    const similaresContent = document.getElementById('similares-content');
    const scrollbarThumb = document.getElementById('scrollbar-thumb');
    const scrollbarTrack = document.getElementById('scrollbar-track');
    const canchasCounter = document.getElementById('canchas-counter');
    
    if (!similaresContainer || !similaresContent || !scrollbarThumb) {
        return; // Si no existe la sección, no hacer nada
    }
    
    let isDragging = false;
    let startY = 0;
    let startTop = 0;
    
    // Calcular la altura del thumb basada en el contenido
    function updateScrollbarThumb() {
        const contentHeight = similaresContent.scrollHeight;
        const containerHeight = similaresContent.clientHeight;
        const trackHeight = scrollbarTrack.clientHeight;
        
        if (contentHeight <= containerHeight) {
            scrollbarThumb.style.display = 'none';
            return;
        }
        
        scrollbarThumb.style.display = 'block';
        const thumbHeight = Math.max(60, (containerHeight / contentHeight) * trackHeight);
        scrollbarThumb.style.height = thumbHeight + 'px';
        
        updateThumbPosition();
        updateCounter();
    }
    
    // Actualizar la posición del thumb
    function updateThumbPosition() {
        const contentHeight = similaresContent.scrollHeight;
        const containerHeight = similaresContent.clientHeight;
        const trackHeight = scrollbarTrack.clientHeight;
        const thumbHeight = scrollbarThumb.clientHeight;
        
        const scrollRatio = similaresContent.scrollTop / (contentHeight - containerHeight);
        const maxTop = trackHeight - thumbHeight;
        const thumbTop = scrollRatio * maxTop;
        
        scrollbarThumb.style.top = thumbTop + 'px';
    }
    
    // Actualizar el contador de canchas visibles
    function updateCounter() {
        const items = similaresContent.querySelectorAll('.similar-item');
        const containerHeight = similaresContent.clientHeight;
        let visibleItems = 0;
        let firstVisibleIndex = 0;
        
        items.forEach((item, index) => {
            const rect = item.getBoundingClientRect();
            const containerRect = similaresContent.getBoundingClientRect();
            
            if (rect.top < containerRect.bottom && rect.bottom > containerRect.top) {
                if (visibleItems === 0) {
                    firstVisibleIndex = index + 1;
                }
                visibleItems++;
            }
        });
        
        if (canchasCounter) {
            canchasCounter.textContent = `${firstVisibleIndex}-${firstVisibleIndex + visibleItems - 1} de ${items.length}`;
        }
    }
    
    // Event listeners para el scroll del contenido
    similaresContent.addEventListener('scroll', function() {
        updateThumbPosition();
        updateCounter();
    });
    
    // Event listeners para el thumb
    scrollbarThumb.addEventListener('mousedown', function(e) {
        isDragging = true;
        startY = e.clientY;
        startTop = parseInt(scrollbarThumb.style.top) || 0;
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const deltaY = e.clientY - startY;
        const trackHeight = scrollbarTrack.clientHeight;
        const thumbHeight = scrollbarThumb.clientHeight;
        const maxTop = trackHeight - thumbHeight;
        
        let newTop = startTop + deltaY;
        newTop = Math.max(0, Math.min(maxTop, newTop));
        
        scrollbarThumb.style.top = newTop + 'px';
        
        // Actualizar el scroll del contenido
        const scrollRatio = newTop / maxTop;
        const contentHeight = similaresContent.scrollHeight;
        const containerHeight = similaresContent.clientHeight;
        const maxScroll = contentHeight - containerHeight;
        
        similaresContent.scrollTop = scrollRatio * maxScroll;
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
    });
    
    // Event listener para hacer clic en el track
    scrollbarTrack.addEventListener('click', function(e) {
        const rect = scrollbarTrack.getBoundingClientRect();
        const clickY = e.clientY - rect.top;
        const trackHeight = rect.height;
        const thumbHeight = scrollbarThumb.clientHeight;
        
        const scrollRatio = clickY / trackHeight;
        const contentHeight = similaresContent.scrollHeight;
        const containerHeight = similaresContent.clientHeight;
        const maxScroll = contentHeight - containerHeight;
        
        similaresContent.scrollTop = scrollRatio * maxScroll;
    });
    
    // Event listeners para rueda del mouse
    similaresContainer.addEventListener('wheel', function(e) {
        e.preventDefault();
        similaresContent.scrollTop += e.deltaY;
    });
    
    // Inicializar
    updateScrollbarThumb();
    
    // Actualizar en resize
    window.addEventListener('resize', function() {
        setTimeout(updateScrollbarThumb, 100);
    });
    
    // Observar cambios en el contenido
    const observer = new MutationObserver(function() {
        setTimeout(updateScrollbarThumb, 100);
    });
    
    observer.observe(similaresContent, {
        childList: true,
        subtree: true
    });
});
