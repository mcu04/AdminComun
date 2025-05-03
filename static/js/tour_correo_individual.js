document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-correo-individual-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Comprobar que estamos en la URL de Enviar Correo Individual
        if (!/\/comunicacion\/destinatarios\/correo-individual\/\d+\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero a la pantalla de Enviar Correo Individual para este tour.');
        }

      // 2) Abrimos el dropdown “Tutoriales” para que Intro.js calcule bien posiciones
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Definimos los pasos del tour
        introJs().setOptions({
        steps: [
        {
            element: btnTour,  // destacamos el propio enlace del tour
            intro:   '📖 Haz clic en “Tutoriales” para relanzar este tour cuando quieras.',
            position:'bottom'
        },
        {
            element: '#correo-form',
            intro:   '📧 Este es el formulario para enviar un correo individual.',
            position:'top'
        },
        {
            element: 'select[name="destinatario"]',
            intro:   '👤 Aquí elige a quién va dirigido el correo.',
            position:'bottom'
        },
        {
            element: 'input[name="asunto"]',
            intro:   '✏️ Escribe el asunto del correo aquí.',
            position:'bottom'
        },
        {
            element: 'textarea[name="mensaje"]',
            intro:   '✍️ Redacta tu mensaje en este campo.',
            position:'right'
        },
        {
            element: '#file-input',
            intro:   '📎 Selecciona un archivo para adjuntar.',
            position:'right'
        },
        {
            element: '#add-file-btn',
            intro:   '➕ Una vez elegido, pulsa aquí para agregarlo a la lista.',
            position:'bottom'
        },
        {
            element: '#file-list',
            intro:   '📄 Aquí verás los archivos que has agregado.',
            position:'top'
        },
        {
            element: 'button[type="submit"]',
            intro:   '🚀 Cuando todo esté listo, pulsa aquí para enviar el correo.',
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