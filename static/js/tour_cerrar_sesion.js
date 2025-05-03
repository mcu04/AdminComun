// static/js/tour_cerrar_sesion.js
document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-cerrar-sesion-btn');
    const navLogout      = document.getElementById('nav-logout-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
      // 1) Abrimos el menú Tutoriales
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 2) Configuramos el tour
        introJs().setOptions({
        steps: [
        {
            element: btnTour,
            intro: '🔰 Haz clic en “Tutoriales” para relanzar cualquier tour.',
            position: 'bottom'
        },
        {
            element: navLogout,   // <— aquí apuntamos al link de cerrar sesión
            intro: '🔓 Este es el botón de “Cerrar Sesión”: úsalo cuando quieras salir de la plataforma.',
            position: 'bottom'
        }
        ],
        nextLabel: 'Siguiente',
        doneLabel: '¡Entendido!',
        showStepNumbers: false
    })
        .oncomplete(() => bsDropdown.hide())
        .onexit    (() => bsDropdown.hide())
        .start();
    });
});
