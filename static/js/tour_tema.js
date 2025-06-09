// File: static/js/tour_tema.js
document.addEventListener('DOMContentLoaded', () => {
    // 1) El enlace “🌙 Tour Tema” que hemos agregado dentro del <ul> de “Tema”
    const tourBtn     = document.getElementById('tour-modo-oscuro-btn');
        
    // 2) El botón “Tema” (despliega el dropdown con “Claro / Oscuro / Tour Tema”)
    const themeToggle = document.getElementById('boton-modo');

    if (!tourBtn || !themeToggle) {
    console.warn('Tour Tema: faltan elementos en el DOM (tourBtn o themeToggle).');
    return;
    }

    tourBtn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();

    // Al abrir este dropdown, es recomendable que el usuario vea bien dónde está
    // el propio botón “Tema”, así que abrimos manualmente el dropdown.
    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(themeToggle);
    bsDropdown.show();

        // Arrancamos Intro.js con los pasos que corresponden al “Tour Tema”
        introJs().setOptions({
            steps: [
            {
            // 1) Reforzamos al usuario dónde está “Tutoriales” (botón principal),
            //    en caso de que quiera relanzar otro tour.
            element: '#btn-tutorial',
            intro:   '🔰 Pulsa aquí para abrir los tours de cada sección cuando quieras.',
            position:'bottom'
            },
            {
                // 2) Señalamos el propio botón “Tema” (boton-modo)
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
        .onexit(()     => bootstrap.Dropdown.getOrCreateInstance(themeToggle).hide())
        .oncomplete(() => bootstrap.Dropdown.getOrCreateInstance(themeToggle).hide())
        .start();

    });
});
