// static/js/tour_seguimiento_actualizado.js
document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle = document.getElementById('tutorialesDropdown');
    const tourBtn        = document.getElementById('tour-ver-seguimiento-btn');

    if (!tutorialToggle || !tourBtn) {
        console.warn('Tour Seguimiento Actualizado: faltan menú o botón en el DOM.');
        return;
    }
    
    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

    
        const path = window.location.pathname;
        // 1️⃣ Ruta válida?
        if (!/listar\/\d+/.test(path)) {
            return alert('⚠️ Ve primero al listado de Seguimientos Actualizados para este tour.');
        }

        /// 2️⃣ Abre el menú “Tutoriales”
        const bs = bootstrap.Dropdown.getOrCreateInstance(tutorialToggle);
        bs.show();

        // 3️⃣ Ahora, recoge el resto de elementos (si no existen, salta con alerta)
        const inputBuscar    = document.getElementById('input-buscar-seguimiento');
        const btnBuscar      = document.getElementById('btn-buscar-seguimiento');
        const btnReset       = document.getElementById('btn-reset-seguimiento');
        const btnExcel       = document.getElementById('btn-export-seguimiento-excel');
        const tabla          = document.getElementById('seguimientoTabla');
        const btnPdf         = document.getElementById('btn-export-seguimiento-pdf');

    if (![inputBuscar,btnBuscar,btnReset,btnExcel,tabla,btnPdf].every(el=>el)) {
        bs.hide();
        return alert('⚠️ No pude encontrar todos los controles para el Tour Seguimiento Actualizado.');
    }

        // 4️⃣ Y por fin, arranca Intro.js
    introJs()
        .setOptions({
            steps: [
            {
                element: tourBtn,
                intro:    '🔄 Pulsa aquí para volver a iniciar el Tour Seguimiento Actualizado.',
                position: 'bottom'
            },
            {
                element: inputBuscar,
                intro:    '🔍 Aquí puedes buscar por título de seguimiento.',
                position: 'bottom'
            },
            {
                element: btnBuscar,
                intro:    '🖱️ Pulsa “Buscar” para filtrar los resultados.',
                position: 'right'
            },
            {
                element: btnReset,
                intro:    '🔄 Pulsa “Restablecer” para limpiar el filtro.',
                position: 'right'
            },
            {
                element: tabla,
                intro:    '🗂️ Esta es la tabla con todos los seguimientos actualizados.',
                position: 'top'
            },
            {
                element: btnExcel,
                intro:    '📈 Haz clic aquí para exportar la lista a Excel.',
                position: 'left'
            },
            
            {
                element: btnPdf,
                intro:    '📄 Y aquí puedes exportar toda la tabla a PDF.',
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
