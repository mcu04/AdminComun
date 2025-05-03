document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-correo-masivo-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Asegurarnos de estar en la pantalla de Correo Masivo
        if (!/\/comunicacion\/correo-masivo\/\d+\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero a "Enviar Correo Masivo" para este tour.');
    }

      // 2) Abrimos el dropdown “Tutoriales”
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Definimos los pasos del tour
        introJs().setOptions({
        steps: [
        {
            element: btnTour,  // apuntamos al propio enlace de Tour Correo Masivo
            intro:   '📖 Haz clic en “Tutoriales” para relanzar este tour cuando quieras.',
            position:'bottom'
        },
        {
            element: '#correo-masivo-form',
            intro:   '📧 Este es el formulario para enviar correos masivos.',
            position:'top'
        },
        {
            element: 'input[name="destinatarios"]',
            intro:   '☑️ Selecciona uno o varios destinatarios.',
            position:'bottom'
        },
        {
            element: 'input[name="asunto"]',
            intro:   '✏️ Escribe el asunto de tu correo aquí.',
            position:'bottom'
        },
        {
            element: 'textarea[name="mensaje"]',
            intro:   '✍️ Redacta el contenido del correo.',
            position:'right'
        },
        {
            element: '#file-input',
            intro:   '📎 Selecciona un archivo para adjuntar.',
            position:'right'
        },
        {
            element: '#add-file-btn',
            intro:   '➕ Pulsa aquí para agregar el archivo a la lista.',
            position:'bottom'
        },
        {
            element: '#file-list',
            intro:   '📄 Aquí verás los archivos que has añadido.',
            position:'top'
        },
        {
            element: 'button[type="submit"]',
            intro:   '🚀 Cuando todo esté listo, pulsa aquí para enviar el correo masivo.',
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
