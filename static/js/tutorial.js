// static/js/tutorial.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌟 tutorial.js cargado, ruta actual:', window.location.pathname);

    document.getElementById('tour-comunidades-registrar-btn')
        ?.addEventListener('click', e => {
            e.preventDefault();
            tourRegistrarComunidades();
        });

        document .getElementById('tour-crear-seguimiento-btn')
        ?.addEventListener('click', e => {
            e.preventDefault();
            tourCrearSeguimiento();
        });

        document.getElementById('tour-exportar-pdf-btn')
            ?.addEventListener('click', tourExportarPDF);

 // Aquí defines el ID de cada <a> en tu menú y la función que lanza ese tour.
    const tours = {
            'tour-general-btn':                     tourGeneral,
            'tour-login-btn':                       tourIniciarSesion,
            'tour-comunidades-lista-btn':           tourListadoComunidades,
            'tour-comunidades-registrar-btn':       tourRegistrarComunidades,
            'tour-crear-seguimiento-btn':           tourCrearSeguimiento,
            'tour-exportar-pdf-btn':                tourExportarPDF,
            
    };

    Object.entries(tours).forEach(([btnId, fn]) => {
        const btn = document.getElementById(btnId);
        if (!btn) {
            console.warn(`❌ No existe en DOM #${btnId}`);
            return;
        }
        console.log(`🔗 Adjuntando listener a #${btnId}`);
        btn.addEventListener('click', e => {
            e.preventDefault();
            console.log(`🖱 Click en #${btnId}`);
    
            const path = window.location.pathname;
    
          // ─── Validaciones de ruta ─────────────────────────────────────
        if ((btnId === 'tour-general-btn' || btnId === 'tour-login-btn')
            && !/iniciar-?sesion/i.test(path)) {
            return alert("⚠️ Este tour sólo funciona en la página de Login.");
        }
        if (btnId === 'tour-comunidades-lista-btn'
            && !path.includes('/seguimiento/comunidades')) {
            return alert("⚠️ Ve primero al listado de Comunidades.");
        }
        if (btnId === 'tour-comunidades-registrar-btn'
            && !path.includes('/seguimiento/registrar-comunidad')) {
            return alert("⚠️ Ve primero a Registrar Comunidad.");
        }
          // …Añade aquí más validaciones específicas de ruta si hiciera falta…
    
          // Si pasa las validaciones, lanza el tour:
        fn();
        });
    });
    });
    

  // ─── Tours ─────────────────────────────────────────────────────────

function tourGeneral() {
    /*console.log('🚀 Iniciando Tour General'); */
    if (!window.location.pathname.includes('/seguimiento/iniciar-sesion')) {
        return alert("⚠️ El Tour General sólo funciona en la página de Iniciar Sesión.");
    }
    introJs().setOptions({
    steps: [
        {
            intro: `
                🔰 <strong>Bienvenido a AdminComunidad</strong><br>
                Una plataforma pensada para facilitar la gestión de la administracion de edificios y condominios. 
                Controla seguimiento de documentación y archivos importantes, comunicaciones a tiempo real y mantenciones programadas, con tus comunidades de forma centralizada.
            `,
            tooltipClass: 'customIntro'
        },
        {
            element: '#nav-login',
            intro: `
                🔐 <strong>Iniciar Sesión</strong><br>
                Accede con tu usuario y contraseña para entrar al sistema.
            `,
            position: 'bottom'
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
            element: '#tutorialesDropdown',
            intro: `
                📖 <strong>Tutoriales</strong><br>
                Aquí encontrarás tours rápidos para cada módulo del sistema.
            `,
            position: 'left'
        }
    ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Entendido!',
        showStepNumbers: false
    }).start();
    }

    function tourIniciarSesion() {
        // Asegúrate de ejecutarlo sólo en la ruta de login:
        if (!window.location.pathname.includes('/seguimiento/iniciar-sesion')) {
            return alert("⚠️ Este tour sólo funciona en la página de Iniciar Sesión.");
        }
    
        introJs()
            .setOptions({
            steps: [
            {
                // Paso 0: introducción
                intro: `
                    🔐 <strong>Bienvenido al inicio de sesión</strong><br>
                    Para acceder a todas las funcionalidades de AdminComunidad, 
                    primero necesitamos verificar tu identidad.
                `,
                tooltipClass: 'customIntro'
            },
            {
                element: '#input-usuario',
                intro: "👤 <strong>Usuario</strong><br>Ingresa aquí tu nombre de usuario.",
                position: 'right'
            },
            {
                element: '#input-contrasena',
                intro: "🔒 <strong>Contraseña</strong><br>Escribe aquí tu contraseña.",
                position: 'right'
            },
            {
                element: '#btn-iniciar-sesion',
                intro: "▶️ <strong>Entrar</strong><br>Pulsa este botón para iniciar sesión.",
                position: 'bottom'
            }
            ],
            nextLabel: 'Siguiente',
            prevLabel: 'Anterior',
            doneLabel: '¡Listo!',
            showStepNumbers: false
        })
        .start();
    }

function tourListadoComunidades() {
        console.log('🚀 Iniciando Tour Listado Comunidades');

        const btnNuevo = document.getElementById('btn-nueva-comunidad');
        const tabla    = document.getElementById('tabla-comunidades');
        const target   = document.querySelector('#btn-tour-ver-seguimiento');

        // debug rápido en consola
        console.log({ btnNuevo, tabla, target, rect: target?.getBoundingClientRect() });

        if (!btnNuevo || !tabla || !target) {
        return alert("⚠️ No pude encontrar uno de los elementos del tour de Comunidades.");
        }

        // hacemos scroll para centrar
        target.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });


        // 🚀 Lanzamos Intro.js apuntando **directamente** al <a> ya ajustado en CSS
        introJs().setOptions({
            steps: [
                
                {
                element: '#tabla-comunidades',
                intro:   "📋 Aquí verás todas las comunidades disponibles en formato tabla.",
                position:'top'
                },
                {
                element: '#btn-tour-ver-seguimiento',
                intro:   "👁️ Pulsa este botón para ver el seguimiento de una comunidad.",
                position:'right'
                },
                {
                    element: '#btn-nueva-comunidad',
                    intro:   "➕ Haz clic aquí para registrar una nueva comunidad.",
                    position:'bottom'
                },
            ],
                nextLabel: 'Siguiente',
                prevLabel: 'Anterior',
                doneLabel: '¡Entendido!',
                showStepNumbers: false,
                scrollToElement: true       
        }).start();
        }



function tourRegistrarComunidades() {
                    console.log('🚀 Iniciando Tour Registrar Comunidad');
                
                    const dropdownToggle = document.getElementById('tutorialesDropdown');
                    const form           = document.getElementById('form-comunidad');
                    const btnGuardar     = document.getElementById('btn-guardar-comunidad');
                    const campoNombre    = document.getElementById('input-nombre-comunidad');
                
                    if (!dropdownToggle || !form || !btnGuardar || !campoNombre) {
                        return alert("⚠️ No encontré uno de los elementos necesarios para el Tour Registrar Comunidad.");
                    }
                
                    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
                
                    introJs()
                        .setOptions({
                            steps: [
                                {
                                    element: dropdownToggle,
                                    intro: "📋 Haz click aquí en “Tutoriales” para relanzar este tour cuando quieras.",
                                    position: 'bottom'
                                },
                                {
                                    element: campoNombre,
                                    intro: "✍️ Escribe aquí el nombre de tu nueva comunidad.",
                                    position: 'right'
                                },
                                {
                                    element: btnGuardar,
                                    intro: "💾 Cuando termines, pulsa aquí para guardar.",
                                    position: 'bottom'
                                }
                            ],
                            nextLabel: 'Siguiente',
                            prevLabel: 'Anterior',
                            doneLabel: '¡Registrado!',
                            scrollToElement: true
                        })
                        .onbeforechange(function(targetElement) {
                            // justo antes del paso 2 (index 1), abrimos el menú de tutoriales
                            if (this._currentStep === 1) {
                                bsDropdown.show();
                            }
                        })
                        .oncomplete(() => bsDropdown.hide())
                        .onexit(()     => bsDropdown.hide())
                        .start();
                }
                
                

// Tour Crear Seguimiento
function tourCrearSeguimiento() {
    console.log('🚀 Iniciando Tour Crear Seguimiento');

    // Paso 1: botón en menú
    const dropdownToggle = document.getElementById('tutorialesDropdown');
    // Paso 2: formulario completo
    const form = document.getElementById('form-seguimiento');
    // Paso 3: campo documentos relacionados
    const docs    = document.getElementById('id_documentacion');
    // Paso 4: checkbox existe
    const existe  = document.getElementById('id_existe');
    // Paso 5: textarea observaciones
    const obs     = document.getElementById('id_observaciones');
    // Paso 6: botón guardar
    const btnGuardar = document.getElementById('btn-guardar-seguimiento');

    if (!dropdownToggle|| !form || !docs || !existe || !obs || !btnGuardar) {
        return alert('⚠️ No pude encontrar todos los elementos para el Tour Crear Seguimiento.');
    }

    // Abrimos el menú "Tutoriales"
    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownToggle);
    bsDropdown.show();

    // Si tu dropdown de "Tutoriales" debe abrirse, puedes hacerlo igual que antes
    // const dropdownToggle = document.getElementById('tutorialesDropdown');
    // bootstrap.Dropdown.getOrCreateInstance(dropdownToggle).show();

    introJs().setOptions({
        steps: [
        {
            element: dropdownToggle,
            intro:    "🔄 Pulsa aquí para volver a iniciar el Tour Crear Seguimiento.",
            position: 'bottom'
        },
        {
            element: docs,
            intro: '📄 Selecciona el documento relacionado: estos son los registros clave que debes gestionar.',
            position: 'bottom'
        },
        {
            element: existe,
            intro: '✅ Marca esta casilla si el documento ya existe para agilizar el control de archivos.',
            position: 'right'
        },
        {
            element: obs,
            intro: '✍️ Añade aquí observaciones útiles que servirán en el seguimiento posterior.',
            position: 'top'
        },
        {
            element: btnGuardar,
            intro: '💾 Cuando hayas completado, pulsa aquí para guardar tu seguimiento.',
            position: 'bottom'
        }
    ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Creado!',
        scrollToElement: true
    })
    .onexit(   () => bsDropdown.hide())
    .oncomplete(() => bsDropdown.hide())
    .start();
}

// Engancha el tour al botón del menú
document.getElementById('tour-crear-seguimiento-btn')
        .addEventListener('click', tourCrearSeguimiento);

function tourExportarPDF() {
    console.log('🚀 Iniciando Tour Exportar PDF');

    // 1) Referencias
    const toggle    = document.getElementById('tutorialesDropdown');
    const menu      = document.querySelector('.tutorial-dropdown-menu');
    const tourItem  = document.getElementById('tour-exportar-pdf-btn');
    const exportBtn = document.getElementById('btn-export-seguimiento-pdf');

    if (!toggle || !menu || !tourItem || !exportBtn) {
        return alert("⚠️ No he podido encontrar uno de los elementos para el Tour Exportar PDF.");
    }

    // 2) Cambiamos la alineación a 'start' para que el menú quede justo bajo el toggle
    menu.classList.remove('dropdown-menu-end');
    menu.classList.add('dropdown-menu-start');

    // 3) Abrimos el dropdown
    const bsDropdown = bootstrap.Dropdown.getOrCreateInstance(toggle);
    bsDropdown.show();

    // 4) Lanzamos Intro.js con pasos bien apuntados
    introJs()
    .setOptions({
        steps: [
        {
            element: toggle,
            intro:    "🔄 Pulsa aquí para relanzar el Tour Exportar PDF en cualquier módulo.",
            position: 'bottom'
        },
        {
            element: tourItem,
            intro:    "📄 Este es el elemento “Tour Exportar PDF” dentro del menú de Tutoriales.",
            position: 'right'
        },
        {
            element: exportBtn,
            intro:    "📥 Usa este botón para generar y descargar un PDF con tu listado de seguimientos, fundamental para reportar o compartir documentación.",
            position: 'left'
        }
        ],
            nextLabel:     'Siguiente',
            prevLabel:     'Anterior',
            doneLabel:     'Entendido',
            showStepNumbers: false,
            scrollToElement: true
    })
        // 5) Antes de cada cambio de paso, si vamos al índice 1, volvemos a abrir el dropdown
    .onbeforechange(function() {
        if (this._currentStep === 1) {
            bsDropdown.show();
            tourItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        })

      // 6) Al salir o completar, lo cerramos y restauramos clases
        .onexit(() => {
        bsDropdown.hide();
        menu.classList.remove('dropdown-menu-start');
        menu.classList.add('dropdown-menu-end');
        })
        .oncomplete(() => {
        bsDropdown.hide();
        menu.classList.remove('dropdown-menu-start');
        menu.classList.add('dropdown-menu-end');
        })

        .start();
    }



    



