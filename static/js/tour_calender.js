document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-calender-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Verificar que estemos en /mantenimiento/calendario/<id>/
        if (!/\/mantenimiento\/calendario\/\d+\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al Calendario de Mantenciones para este tour.');
        }

      // 2) Abrimos el dropdown de “Tutoriales”
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Dejamos que FullCalendar renderice (500 ms suele bastar)
        await new Promise(res => setTimeout(res, 500));

      // 4) Configuramos y arrancamos Intro.js
        const tour = introJs().setOptions({
        steps: [
            {
                // ➤ Paso 0: referencia al botón Tour dentro de Tutoriales
            element: btnTour,
            intro:   '🔄 Pulsa aquí para relanzar este Tour Calendario Mantenciones cuando quieras.',
            position:'bottom'
            },
            {
                // ➤ Paso 1: apuntamos al div principal del calendario
            element: '#calendar',
            intro:   '🗓️ Este es tu Calendario de Mantenciones: aquí ves programadas las fechas.',
            position:'top'
            },
            {
                // ➤ Paso 2: “Hoy”
            element: '.fc-today-button',
            intro:   '⏱️ Pulsa “Hoy” para saltar de vuelta al mes actual.',
            position:'bottom'
            },
            {
                // ➤ Paso 3: cambio de vista
            element: '.fc-dayGridMonth-button',
            intro:   '🌄 Con “Mes” ves todo el mes a la vez.',
            position:'bottom'
            },
            {
                // ➤ Paso 4: cambio de vista semana
            element: '.fc-timeGridWeek-button',
            intro:   '📆 Con “Semana” ves sólo la semana actual.',
            position:'bottom'
            },
            {
                // ➤ Paso 5: cambio de vista eventos semanales
            element: '.fc-listWeek-button',
            intro:   '📋 Con “Lista” obtienes un listado de eventos semanales.',
            position:'bottom'
            },
            {
                /*// ➤ Paso 6: tarjetas de evento
                element: '.fc-event',
                intro:   '🔵 Haz clic en un evento para ver sus detalles en un modal.',
                position:'auto' */
            },
            
        ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Listo!',
        showStepNumbers: false,
        scrollToElement: true,
        overlayOpacity: 0.6
    })
    /*// Antes del paso 6, simulamos click para abrir el modal
    .onbeforechange(function(targetElement) {
        if (this._currentStep === 6) {
        // el primer evento
        const evt = document.querySelector('.fc-event');
        if (evt) evt.click();
    }
    })
    // Al cerrar el tour, cerramos el modal y el dropdown
    .onexit(() => {
        bsDropdown.hide();
        const modalEl = document.getElementById('eventModal');
        bootstrap.Modal.getInstance(modalEl)?.hide();
    })
    .oncomplete(() => {
        bsDropdown.hide();
        bootstrap.Modal.getInstance(document.getElementById('eventModal'))?.hide();
    }) */
    .start();
    });
});