document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-subir-archivo-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Verificar URL de subida
        if (!/\/biblioteca\/\d+\/subir\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al formulario de Subir Archivo para este tour.');
        }

      // 2) Abrir dropdown para que Intro.js calcule bien posición
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Configurar pasos
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro:   '📤 Haz clic en “Tutoriales” para relanzar este tour cuando quieras.',
            position:'bottom'
        },
        {
            element: '#subir-archivo-title',
            intro:   '🗂️ Aquí defines el tipo de documento que vas a subir.',
            position:'bottom'
        },
        {
            element: '#id_tipo',
            intro:   '🔖 Selecciona el Area del archivo.',
            position:'right'
        },
        {
            element: '#id_categoria',
            intro:   '📂 Elige la categoría bajo la que quedará registrado.',
            position:'right'
        },
        {
            element: '#id_titulo_documento',
            intro:   '✏️ Escribe un título claro para tu documento.',
            position:'bottom'
        },
        {
            element: '#id_documento',
            intro:   '📎 Selecciona el archivo de tu disco para subirlo.',
            position:'bottom'
        },
        {
            element: '#btn-subir-archivo',
            intro:   '🚀 Finalmente, haz clic aquí para subir el archivo.',
            position:'right'
        },
        {
            element: '#btn-volver-biblioteca',
            intro:   '🔙 Y aquí puedes volver a la Biblioteca en cualquier momento.',
            position:'left'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Listo!',
        showStepNumbers:false,
        scrollToElement:true
    })
        .onexit(()     => bsDropdown.hide())
        .oncomplete(() => bsDropdown.hide())
        .start();
    });
});
