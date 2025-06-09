// static/js/tour_general.js
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('tour-general-btn');
    const tutorialBtn = document.getElementById('btn-tutorial'); // el botón único “📖 Tutorial”
    if (!btn || !tutorialBtn) return;

    btn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();

    // 1️⃣ Validación de ruta
    if (!/^\/auth\/iniciar-sesion\/?$/.test(window.location.pathname)) {
        return alert('⚠️ El Tour General solo funciona en la página de Login.');
    }

    // 2️⃣ Lanzar Intro.js
    introJs().setOptions({
        steps: [
        { intro: '🔰 <strong>Bienvenido a AdminComunidad</strong><br> Una plataforma pensada para facilitar la gestión de la administracion de edificios y condominios. Controla seguimiento de documentación y archivos importantes, comunicaciones en tiempo real y mantenciones programadas, con tus comunidades de forma centralizada.', tooltipClass: 'customIntro' 
        },
        {
        element: '#nav-login',
        intro: ' 🔐 <strong>Iniciar Sesión</strong><br> Accede con tu usuario y contraseña para entrar al sistema, previamente debes leer y aceptar los terminos y condiciones.', 
        position: 'bottom',
        },
        {
        element: '#nav-contacto',
        intro: `
        📞 <strong>Contacto</strong><br>
        ¿Dudas? Escríbenos al equipo de soporte.
        `,
        position: 'bottom'
        },
        {
        element: '#boton-modo',
        intro: `
        🌗 <strong>Modo Claro / Oscuro</strong><br>
        Ajusta la apariencia según tu preferencia o condiciones de luz.
        `,
        position: 'left'
        },
        {
        element: '#btn-tutorial',
        intro: `
        📖 <strong>Tutoriales</strong><br>
        Aquí encontrarás tours rápidos para cada módulo del sistema.
        `,
        position: 'left'
        },
        ],

        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Entendido!',
        showStepNumbers: false
    })
        .start();
    });
});
