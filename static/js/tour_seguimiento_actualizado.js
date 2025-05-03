// static/js/tour_seguimiento_actualizado.js
document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle = document.getElementById('tutorialesDropdown');
    const tourBtn        = document.getElementById('tour-ver-seguimiento-btn');
    const inputBuscar    = document.getElementById('input-buscar-seguimiento');
    const btnBuscar      = document.getElementById('btn-buscar-seguimiento');
    const btnReset       = document.getElementById('btn-reset-seguimiento');
    const btnExcel       = document.getElementById('btn-export-seguimiento-excel');
    const tabla          = document.getElementById('seguimientoTabla');
    const btnPdf         = document.getElementById('btn-export-seguimiento-pdf');

    if (![tutorialToggle,tourBtn,inputBuscar,btnBuscar,btnReset,btnExcel,tabla,btnPdf].every(el=>el)) {
        console.warn('Tour Seguimiento Actualizado: faltan elementos en el DOM.');
        return;
    }

    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // Abrimos el dropdown “Tutoriales”
        const bs = bootstrap.Dropdown.getOrCreateInstance(tutorialToggle);
        bs.show();

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
        .onexit    (() => bs.hide())
        .oncomplete(() => bs.hide())
        .start();
    });
});
