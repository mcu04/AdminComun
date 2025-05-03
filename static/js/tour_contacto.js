document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-modulo-contacto-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Comprobar que estamos en la ruta de Contacto
        if (!/\/contacto\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero al módulo de Contacto para este tour.');
        } 

      // 2) Abrir el dropdown de “Tutoriales” para que Intro.js posicione bien
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Configurar y arrancar el tour
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro:   '✉️ Haz clic en “Tutoriales” para relanzar cualquier tour cuando quieras.',
            position:'bottom'
        },
        {
            element: 'h1.text-center',
            intro:   '📬 Esta es la página de Contacto, donde nos envías tus consultas a soporte.',
            position:'bottom'
        },
        {
            element: '#nombre',
            intro:   '👤 Aquí indicas tu nombre.',
            position:'right'
        },
        {
            element: '#email',
            intro:   '📧 Ingresa tu correo electrónico para que podamos responderte.',
            position:'right'
        },
        {
            element: '#mensaje',
            intro:   '💬 Escribe tu mensaje o sugerencia aquí.',
            position:'top'
        },
        {
            element: 'button[type="submit"]',
            intro:   '🚀 Finalmente, pulsa aquí para enviar tu mensaje.',
            position:'bottom'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Enviado!',
        showStepNumbers:false,
        scrollToElement:true,
        overlayOpacity:0.5
    })
        .oncomplete(() => bsDropdown.hide())
        .onexit    (() => bsDropdown.hide())
        .start();
    });
});