// File: static/js/tour_recuperar_contrasena.js
document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle   = document.getElementById('tutorialesDropdown');
    const tourBtn          = document.getElementById('tour-recuperar-contrasena-btn');
    const inputEmail       = document.getElementById('email');
    const btnEnviarEnlace  = document.getElementById('btn-enviar-enlace');

    if (!tutorialToggle || !tourBtn) {
        console.warn('Tour Recuperar Contraseña: faltan elementos en el DOM.');
        return;
    }

    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

           // Validación de ruta
    if (!window.location.pathname.includes('/seguimiento/password_reset')) {
        return alert('⚠️ Este tour sólo funciona en la página de Restablecer Contraseña.');
        }

      // 1️⃣ Abrimos el menú “Tutoriales”
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(tutorialToggle);
        bsDropdown.show();

      // 2️⃣ Esperamos un pelín para asegurar que Bootstrap despliegue el menú
        setTimeout(() => {
        introJs().setOptions({
            steps: [
            {
                element: tutorialToggle,
                intro: '🔰 Pulsa aquí en “Tutoriales” para relanzar este tour cuando quieras.',
                position: 'bottom'
            },
            {
                element: inputEmail,
                intro: '📧 Introduce aquí tu correo electrónico para recibir el enlace de recuperación.',
                position: 'bottom'
            },
            {
                element: btnEnviarEnlace,
                intro: '🚀 Pulsa aquí para enviar el enlace de restablecimiento de contraseña.',
                position: 'bottom'
            }
        ],
            nextLabel: 'Siguiente',
            prevLabel: 'Anterior',
            doneLabel: '¡Listo!',
            showStepNumbers: false,
            scrollToElement: true,
            overlayOpacity: 0.6
        })
        .onexit(()     => bsDropdown.hide())
        .oncomplete(() => bsDropdown.hide())
        .start();
    }, 150);
    });
});
