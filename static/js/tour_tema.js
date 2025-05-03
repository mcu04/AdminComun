// File: static/js/tour_tema.js
document.addEventListener('DOMContentLoaded', () => {
    const tutorialToggle = document.getElementById('tutorialesDropdown');
    const tourBtn        = document.getElementById('tour-modo-oscuro-btn');
    const themeToggle    = document.getElementById('boton-modo');
    

    if (!tutorialToggle || !tourBtn || !themeToggle ) {
        console.warn('Tour Tema: faltan elementos en el DOM.');
        return;
    }

    tourBtn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

        //  Arrancamos el tour
        introJs().setOptions({
            steps: [
            {
                element: tutorialToggle,
                intro:   '🔰 Abre “Tutoriales” para relanzar cualquier recorrido cuando quieras.',
                position:'bottom'
            },
            {
                element: themeToggle,
                intro:   '🌙 Haz clic en “Tema” para cambiar entre Modo Claro y Oscuro, 🌘 Selecciona “Modo Oscuro” para activar la vista nocturna, ☀️ Selecciona “Modo Claro” para restaurar la vista diurna.',
                position:'bottom'
            },
            
        ],
            nextLabel:      'Siguiente',
            prevLabel:      'Anterior',
            doneLabel:      '¡Listo!',
            showStepNumbers:false,
            scrollToElement:true,
            overlayOpacity: 0.5
        })
        .start();

    });
});
