// static/js/tour_informe.js
document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-informe-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Después: comprueba /mantenimiento/mantencion/informe/{id}/
        if (!/\/mantenimiento\/mantencion\/informe\/\d+\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al Informe de Mantenciones para este tour.');
        }

      // 2) Abrimos el dropdown de Tutoriales
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Definimos los pasos del tour
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro:   '🔄 Pulsa aquí para volver a lanzar el Tour Informe Mantenciones.',
            position:'bottom'
        },
        {
            element: '#filterForm',
            intro:   '🔍 Usa estos filtros (Año / Mes) para acotar tu informe.',
            position:'bottom'
        },
        {
            element: '#informeTable',
            intro:   '📋 Aquí tienes la tabla con todos los datos de mantenciones.',
            position:'top'
        },
        {
            element: '.dt-buttons .buttons-excel',
            intro:   '📊 Exporta tus datos a Excel para analizarlos fuera del sistema.',
            position:'bottom'
        },
        {
            element: '.dt-buttons .buttons-pdf',
            intro:   '📄 Genera un PDF de este informe, listo para imprimir o compartir.',
            position:'bottom'
        },
        {
            element: '.dt-buttons .buttons-print',
            intro:   '🖨️ Imprime directamente desde aquí si lo necesitas en papel.',
            position:'bottom'
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
