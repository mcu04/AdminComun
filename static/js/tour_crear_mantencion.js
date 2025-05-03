document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-crear-mantencion-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Comprobar que estamos en la URL de creación de mantención
        if (!/\/mantenimiento\/comunidad\/\d+\/mantenciones\/nueva\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al formulario de “Nueva Mantención Preventiva” para este tour.');
        }

      // 2) Abrimos el dropdown “Tutoriales”
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Definimos los pasos
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro:   '✍️ Este tour te guiará por el formulario de Nueva Mantención.',
            position:'bottom-start'
        },
        {
            element: '#titulo-mantencion',
            intro:   '📝 Aquí ves si estás creando o editando una mantención preventiva.',
            position:'right'
        },
        {
            element: '#id_category',
            intro:   '⚙️ Selecciona la instalación predefinida de este checklist.',
            position:'bottom'
        },
        {
            element: '#input-otra-instalacion',
            intro:   '🏷️ Si la instalación no está en el listado, indícala aquí.',
            position:'bottom'
        },
        {
            element: '#input-fecha-programada',
            intro:   '📆 Selecciona la fecha programada para realizarla.',
            position:'bottom'
        },
        {
            element: '#textarea-descripcion',
            intro:   '✏️ Describe brevemente el alcance de esta mantención.',
            position:'right'
        },
        {
            element: '#textarea-observaciones',
            intro:   '💬 Añade observaciones adicionales tras la ejecución.',
            position:'right'
        },
        {
            element: '#form-mantencion',
            intro:   '📂 Revisa todos los campos antes de guardar.',
            position:'top'
        },
        {
            element: '#btn-guardar-mantencion',
            intro:   '💾 Cuando estés listo, pulsa aquí para guardar la mantención.',
            position:'bottom'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Hecho!',
        showStepNumbers:false,
        scrollToElement:true
    })
        .onexit(()     => bsDropdown.hide())
        .oncomplete(() => bsDropdown.hide())
        .start();
    });
});
