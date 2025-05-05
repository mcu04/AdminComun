document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle = document.getElementById('tutorialesDropdown');
    const tourBtn        = document.getElementById('tour-ver-seguimiento-pendiente-btn');

    if (!tutorialToggle || !tourBtn) {
        console.warn('Tour Seguimiento Pendiente: faltan menú o botón en el DOM.');
        return;
    }


    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

        //  ➡️ Validar ruta
        const path = window.location.pathname;
        // 1️⃣ Ruta válida?
        if (!/pendiente\/\d+/.test(path)) {
            return alert('⚠️ Ve primero al listado de Seguimientos Pendientes para este tour.');
        }

        // 2️⃣ Abre “Tutoriales”
        const bs = bootstrap.Dropdown.getOrCreateInstance(tutorialToggle);
        bs.show();

        // 3️⃣ Recoge el resto de elementos
        const inputBuscar    = document.getElementById('input-buscar-seguimiento-pendiente');
        const btnBuscar      = document.getElementById('btn-buscar-seguimiento-pendiente');
        const btnReset       = document.getElementById('btn-reset-seguimiento-pendiente');
        const btnExcel       = document.getElementById('btn-export-seguimiento-pendiente-excel');
        const tabla          = document.getElementById('seguimientoTabla');
        const btnPdf         = document.getElementById('btn-export-seguimiento-pendiente-pdf');

    if (![inputBuscar,btnBuscar,btnReset,btnExcel,tabla,btnPdf].every(el=>el)) {
        bs.hide();
        return alert('⚠️ No pude encontrar todos los controles para el Tour Seguimiento Pendiente.');
    }

        // 4️⃣ Lanzar Intro.js
        introJs()
        .setOptions({
            steps: [
            {
                element: tourBtn,
                intro:    '🔄 Pulsa aquí para reiniciar el Tour Seguimiento Pendiente.',
                position: 'bottom'
            },
            {
                element: inputBuscar,
                intro:    '🔍 Usa este campo para buscar por título de seguimiento.',
                position: 'bottom'
            },
            {
                element: btnBuscar,
                intro:    '🖱️ Pulsa “Buscar” para filtrar los resultados.',
                position: 'right'
            },
            {
                element: btnReset,
                intro:    '🔄 Pulsa “Restablecer” para borrar el filtro.',
                position: 'right'
            },
            {
                element: tabla,
                intro:    '🗂️ Esta tabla muestra todos los seguimientos pendientes.',
                position: 'top'
            },
            {
                element: btnExcel,
                intro:    '📈 Exporta la lista a Excel aquí.',
                position: 'left'
            },
            {
                element: btnPdf,
                intro:    '📄 Exporta la tabla a PDF desde este botón.',
                position: 'bottom'
            }
        ],
            nextLabel:      'Siguiente',
            prevLabel:      'Anterior',
            doneLabel:      '¡Listo!',
            scrollToElement: true,
            overlayOpacity: 0.5
        })
        .onexit(()     => bs.hide())
        .oncomplete(() => bs.hide())
        .start();
    });
});
