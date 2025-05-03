document.addEventListener('DOMContentLoaded', () => {
    // 1) El toggle del menú “Tutoriales”
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    // 2) El ítem de nuestro tour dentro del menú
    const btnTour         = document.getElementById('tour-mantencion-preventiva-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', (e) => {
      // ➡️ Evitamos que bootstrap cierre el dropdown al hacer click
        e.preventDefault();
        e.stopPropagation();

      // 3) Solo seguimos si estamos en la URL correcta
        if (!/^\/mantenimiento\/comunidad\/\d+\/mantenciones\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al listado de Mantención Preventiva Instalaciones para este tour.');
        }

      // 4) Abrimos manualmente el dropdown
    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
    bsDropdown.show();

      // 5) Arrancamos Intro.js
    introJs()
        .setOptions({
            steps: [
            {
              // **Ahora sí**, señalamos el botón “Tutoriales”
            element: btnTour,
            intro:   '📖 Haz click aquí en “Tutoriales” para relanzar este Tour cuando quieras.',
            position:'bottom-start'
            },
            {
            element: '#mant-list-title',
            intro:   '📋 Aquí ves el título de la sección de Mantenciones Preventivas.',
            position:'bottom'
            },
            {
            element: '#btn-nueva-mantencion',
            intro:   '➕ Pulsa aquí para crear una **nueva** mantención preventiva.',
            position:'right'
            },
            {
            element: '#filtro',
            intro:   '🔎 Usa este desplegable para filtrar según el estado.',
            position:'bottom'
            },
            {
            element: '#btn-filtrar',
            intro:   '🖱️ Aplica el filtro para ver solo las mantenciones que necesites.',
            position:'left'
            },
            {
            element: '#tabla-mantenciones',
            intro:   '📑 Esta es la tabla con todas tus mantenciones según el filtro.',
            position:'top'
            },
            {
            element: '#tabla-mantenciones tbody tr:first-child .btn-primary',
            intro:   '✏️ Edita la primera mantención desde este botón.',
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
