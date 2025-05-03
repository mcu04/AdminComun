document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle = document.getElementById('tutorialesDropdown');
    const tourBtn        = document.getElementById('tour-ver-seguimiento-pendiente-btn');
    const inputBuscar    = document.getElementById('input-buscar-seguimiento-pendiente');
    const btnBuscar      = document.getElementById('btn-buscar-seguimiento-pendiente');
    const btnReset       = document.getElementById('btn-reset-seguimiento-pendiente');
    const btnExcel       = document.getElementById('btn-export-seguimiento-pendiente-excel');
    const tabla          = document.getElementById('seguimientoTabla');
    const btnPdf         = document.getElementById('btn-export-seguimiento-pendiente-pdf');

    // Verificamos que todos existan
    if (![tutorialToggle,tourBtn,inputBuscar,btnBuscar,btnReset,btnExcel,tabla,btnPdf].every(el=>el)) {
        console.warn('Tour Seguimiento Pendiente: faltan elementos en el DOM.');
        return;
    }

    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1️⃣ Abrimos “Tutoriales” para relanzar este tour
        const bsTut = bootstrap.Dropdown.getOrCreateInstance(tutorialToggle);
        bsTut.show();

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
        .onexit    (() => bsTut.hide())
        .oncomplete(() => bsTut.hide())
        .start();
    });
});
