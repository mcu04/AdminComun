document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    const btnTour        = document.getElementById('tour-gestionar-destinatarios-btn');
    if (!dropdownToggle || !btnTour) return;

    btnTour.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

      // 1) Verificamos que estemos en la URL correcta:
      //    /comunidad/<id>/gestionar_destinatarios/  (ajusta si es distinto)
        if (!/\/comunidad\/\d+\/destinatarios\/?$/.test(window.location.pathname)) {
        return alert('⚠️ Ve primero a la pantalla de “Gestión de Destinatarios” para este tour.');
        }

      // 2) Abrimos el dropdown de Tutoriales
        const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
        bsDropdown.show();

      // 3) Configuramos y lanzamos Intro.js
        introJs()
        .setOptions({
            steps: [
            {
                element: btnTour,
                intro:   '➕ Este tour te guiará por la Gestión de Destinatarios.',
                position:'bottom-start'
            },
            {
                element: 'h2',
                intro:   '👥 Aquí ves el título de la sección.',
                position:'bottom'
            },
            {
                element: 'form',
                intro:   '✍️ Rellena este formulario para **agregar** un nuevo destinatario.',
                position:'top'
            },
            {
                element: 'button.btn-success',
              intro:   '💾 Haz clic para **guardar** el destinatario.',
                position:'right'
            },
            {
                element: 'h3',
                intro:   '📋 Aquí tienes la lista de destinatarios ya registrados.',
                position:'bottom'
            },
            {
                element: 'table.table tbody tr:first-child td:last-child a.btn-primary',
                intro:   '✏️ Usa este botón para **editar** el primer destinatario.',
                position:'left'
            },
            {
                element: 'table.table tbody tr:first-child td:last-child a.btn-danger',
                intro:   '🗑️ Usa este botón para **eliminar** el primer destinatario.',
                position:'left'
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
