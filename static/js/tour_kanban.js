document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-kanban-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();

    // 1) Asegurarnos de estar en la vista Kanban
    if (!/^\/mantenimiento\/kanban\/\d+\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al Tablero Kanban de Mantenimiento para este tour.');
    }

      // 2) Abrimos el menú Tutoriales
    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
    bsDropdown.show();

      // 3) Definimos pasos
    introJs().setOptions({
        steps: [
        {
            element: dropdownToggle,
            intro:   '📖 Haz click en “Tutoriales” para relanzar este tour cuando quieras.',
            position:'bottom'
        },
        {
            element: '#kanban-title',
            intro:   '📊 Bienvenido al **Tablero Kanban** de Mantenimiento; aquí organizas tus mantenciones por estado.',
            position:'bottom'
        },
        {
            element: '#col-pendientes',
            intro:   '⏳ **Pendientes**: mantenciones aún por hacer.',
            position:'top'
        },
        {
            element: '#col-proceso',
            intro:   '🔄 **En Proceso**: mantenciones en ejecución.',
            position:'top'
        },
        {
            element: '#col-revision',
            intro:   '🔍 **Revisión**: mantenciones a verificar antes de cerrar.',
            position:'top'
        },
        {
            element: '#col-completado',
            intro:   '✅ **Completadas**: mantenciones ya finalizadas.',
            position:'top'
        },
        {
            element: '.kanban-card.card',
            intro:   '✏️ Arrastra o edita cualquier tarjeta para cambiar de estado.',
            position:'right'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Entendido!',
        showStepNumbers:false,
        scrollToElement:true,
        overlayOpacity: 0.6
    })
        .oncomplete(() => bsDropdown.hide())
        .onexit(()     => bsDropdown.hide())
        .start();
    });
});
