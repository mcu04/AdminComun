document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-biblioteca-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // Asegurarnos de estar en la vista de la Biblioteca
        if (!/\/biblioteca\/biblioteca\/\d+\/archivos\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero a la Biblioteca de Archivos para este tour.');
    }

      // 1) Abrimos el dropdown “Tutoriales”
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 2) Lanzamos Intro.js con los pasos
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro:   '📤 Pulsa aquí para relanzar el Tour Biblioteca en cualquier momento.',
            position:'bottom'
        },
        {
            element: 'a[title="Subir Archivo"]',
            intro:   '➕ Usa este botón para subir un nuevo archivo a la biblioteca.',
            position:'left'
        },
        {
            element: 'table.table',
            intro:   '📚 Aquí encontrarás la lista de todos los archivos disponibles.',
            position:'top'
        },
        {
            element: '.bi-download',
            intro:   '⬇️ Usa este icono para descargar el archivo directamente.',
            position:'auto'
        },
        {
            element: 'button.btn-danger',
            intro:   '🗑️ Pulsa este botón para eliminar un archivo de la biblioteca.',
            position:'auto'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Entendido!',
        showStepNumbers:false,
        scrollToElement:true,
        overlayOpacity:0.6
    })
        .onexit(()     => bsDropdown.hide())
        .oncomplete(() => bsDropdown.hide())
        .start();
    });
});
