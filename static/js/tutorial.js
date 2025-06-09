// static/js/tutorial.js
// Centraliza todos los tours en un único archivo y botón "Tutorial"
// Solo se lanza el tour correspondiente según la URL actual.

console.log("✅ tutorial.js arranca");

document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ DOM listo — tutorial.js");

    const btn = document.getElementById('btn-tutorial');
    if (!btn) return console.warn("❌ No encontré #btn-tutorial");

    btn.addEventListener('click', e => {
    e.preventDefault();

    // ←––––– AQUÍ: ¡DEBUG DEL CLICK!
    console.log('👉 click en btn-tutorial detectado en', window.location.pathname);

    // —— LOG INICIAL PARA VERIFICAR CLICK Y PATH ——
    const path = window.location.pathname;
    console.log("📖 Tutorial pulsado. URL actual:", path);

    // ——————————————————————————————————————————————————————
    // 1) Rutas de Autenticación y Comunidades (return tras lanzar)
    // ——————————————————————————————————————————————————————

    // ---- Autenticación ----
    if (/\/auth\/iniciar-sesion/.test(path)) {
        return tourIniciarSesion();
    }
    // ---- Recuperar contraseña ----
    if (/password_reset/.test(path)) {
        return tourRecuperarContrasena();
    }
    // ---- Comunidades: Actualizar ----
    if (/\/seguimiento\/comunidades\/actualizar\/\d+\/?$/.test(path)) {
        return tourActualizarComunidad();
    }
    // ---- Comunidades: Eliminar ----
    if (/\/seguimiento\/comunidades\/eliminar\/\d+\/?$/.test(path)) {
        return tourEliminarComunidad();
    }
    // ---- Comunidades: Listado (ni actualizar ni eliminar) ----
    if (/^\/seguimiento\/comunidades\/?$/.test(path)) {
        return tourListadoComunidades();
    }
    // ---- Registrar Comunidad ----
    if (/^\/seguimiento\/registrar-comunidad\/?$/.test(path)) {
        return tourRegistrarComunidad();
    }
    
    // ——————————————————————————————————————————————————————
    // 2) Tours de Seguimiento (updated vs pendiente)
    // ——————————————————————————————————————————————————————

    const matchUpdated = /^\/seguimiento\/seguimiento\/listar\/\d+\/?$/.test(path);
    const matchPending = /^\/seguimiento\/pendiente\/\d+\/?$/.test(path);

    if (matchUpdated || matchPending) {
        return runTourSeguimiento(matchUpdated ? "actualizado" : "pendiente");
    }

    // ——————————————————————————————————————————————————————
    // 3) Resto de módulos
    // ——————————————————————————————————————————————————————

    // ---- Crear Seguimiento ----
    if (/\/seguimiento\/crear/.test(path)) {
        return tourCrearSeguimiento();
    }
    // ---- Dashboard Mantenimiento ----
    if (/\/mantenimiento\/comunidad\/\d+\/dashboard/.test(path)) {
        return tourDashboardMantenimiento();
    }
    // ---- Mantención Preventiva ----
    if (/^\/mantenimiento\/comunidad\/\d+\/mantenciones\/?$/.test(path)) {
        return tourMantencionesPreventivas();
    }
    // ---- Tablero Kanban ----
    if (/^\/mantenimiento\/kanban\/\d+\/?$/.test(path)) {
        return tourKanban();
    }
    if (/^\/mantenimiento\/calendario\/\d+\/?$/.test(path)) {
        return tourCalendarioMantenciones();
    }
    // ---- Informe de Mantenciones ----
    if (/^\/mantenimiento\/mantencion\/informe\/\d+\/?$/.test(path)) {
        return tourInformeMantencion();
    }
    // ---- Correo Individual ----
    if (/\/comunicacion\/destinatarios\/correo-individual\/\d+\/?$/.test(path)) {
        return tourCorreoIndividual();
    }
    // ---- Correo Masivo ----
    if (/\/comunicacion\/correo-masivo\/\d+\/?$/.test(path)) {
        return tourCorreoMasivo();
    }
    if (/\/comunicacion\/comunidad\/\d+\/destinatarios\/?$/.test(path)) {
        return tourGestionarDestinatarios();
    }

    // ---- Biblioteca de Archivos ----
    if (/^\/biblioteca\/biblioteca\/\d+\/archivos\/?$/.test(path)) {
        return tourBiblioteca();
    }

    // ---- Subir Archivo ----
    if (/^\/biblioteca\/biblioteca\/\d+\/subir\/?$/.test(path)) {
        return tourSubirArchivo();
    }

    // Contacto
    if (/^\/biblioteca\/contacto\/?$/.test(path)) {
        return tourContacto();
    }

    // Dentro del listener de “btn-tutorial”, en la parte que comprueba rutas:
    if (/^\/auth\/cerrar_sesion\/?$/.test(path)) {
        return tourCerrarSesion();
    }

    // —— Si no matchea ninguna ruta:
    else {
        return alert("⚠️ No hay un tour configurado para esta página.");
    }
    });
});


// ─── Definición de funciones de cada tour ───────────────────────────

function tourIniciarSesion() {
    introJs().setOptions({
        steps: [
        {
            intro: "🔐 <strong>Bienvenido al inicio de sesión</strong><br>\
            Para acceder a todas las funcionalidades de AdminComunidad,\
            primero necesitamos verificar tu identidad.",
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
            element: '#accept-terms',
            intro: "✅ <strong>Acepta los Términos y Condiciones</strong><br>Debes marcar esta casilla antes de continuar.",
            position: 'right'
        },
        {
            element: '#btn-iniciar-sesion',
            intro: "▶️ <strong>Entrar</strong><br>Pulsa este botón para iniciar sesión.",
            position: 'bottom'
        },
        ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Listo!',
        showStepNumbers: false
    })
    .start();
    }

function tourRecuperarContrasena() {
    // 1) Capturamos los elementos de la página
    const inputEmail      = document.getElementById('input-email');  // Ajusta este ID si tu campo tiene otro
    const btnEnviarEnlace = document.getElementById('btn-enviar-enlace'); // Dale un ID a tu botón si no lo tiene

    if (!inputEmail || !btnEnviarEnlace) {
        return alert("⚠️ No pude encontrar los campos para Recuperar Contraseña.");
    }
    introJs().setOptions({
            steps: [
            { 
                intro: "🔑 Recupera tu contraseña si la olvidaste."
            },
            {
                element: inputEmail,
                intro: '📧 Escribe aquí tu correo electrónico para recibir el enlace de recuperación.',
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
        })
    .start();
}

function tourActualizarComunidad() {
    const steps = [
    {
        intro: "✏️ <strong>Actualizar Comunidad</strong><br>Modifica los datos de tu comunidad aquí."
    },
    {
        element: 'form input[name="nombre"]',
        intro: '🏷️ <strong>Nombre</strong>: cambia el nombre de la comunidad.',
        position: 'right'
    },
    {
        element: 'form input[name="direccion"]',
        intro: '📍 <strong>Dirección</strong>: edita la dirección.',
        position: 'right'
    },
    {
      element: 'form #id_descripcion',  // ajusta al id real de tu textarea
        intro: '📝 <strong>Descripción</strong>: aquí puedes actualizar la descripción.',
        position: 'top'
    },
    {
        element: 'button[type="submit"]',
        intro: '💾 <strong>Actualizar</strong>: guarda los cambios.',
        position: 'bottom'
    },
    {
        element: 'a.btn-secondary',
        intro: '🔙 <strong>Volver</strong>: regresa al listado sin guardar.',
        position: 'bottom'
    }
];

    introJs()
    .setOptions({ steps, 
        nextLabel:'Siguiente', 
        prevLabel:'Anterior', 
        doneLabel:'¡Listo!', 
        showStepNumbers:false })
    .start();
}

function tourEliminarComunidad() {
    const steps = [
    {
        intro: "⚠️ <strong>Eliminar Comunidad</strong><br>Esta acción es irreversible."
    },
    {
        element: 'p strong',
        intro: '❗ Comprueba bien que sea la comunidad correcta:',
        position: 'bottom'
    },
    {
        element: 'button.btn-danger',
        intro: '🗑️ <strong>Eliminar</strong>: borra definitivamente la comunidad.',
        position: 'bottom'
    },
    {
        element: 'a.btn-secondary',
        intro: '❌ <strong>Cancelar</strong>: vuelve al listado sin cambios.',
        position: 'bottom'
    }
];

    introJs()
    .setOptions({ steps, 
        nextLabel:'Siguiente', 
        prevLabel:'Anterior', 
        doneLabel:'¡Hecho!', 
        showStepNumbers:false })
    .start();
}

function tourListadoComunidades() {
    const tutorialToggle = document.getElementById('btn-tutorial');

    introJs().setOptions({
        steps: [
        { 
            intro: "🏘️ Listado de tus comunidades."
        },
                {
        element: '#tabla-comunidades',
        intro:  "📋 Aquí verás todas las comunidades disponibles en formato tabla.",
        position:'top'
        },
        {
        element: '#btn-tour-ver-seguimiento',
        intro: "👁️ Pulsa este botón para ver el seguimiento de una comunidad.",
        position:'right'
        },
        {
        element: '#btn-tour-actualizar-comunidad',
        intro: "👁️ Pulsa este botón para actualizar una comunidad.",
        position:'right'
        },
        {
        element: '#btn-tour-eliminar-comunidad',
        intro: "👁️ Pulsa este botón para eliminar una comunidad.",
        position:'right'
        },
        {
        element: '#btn-nueva-comunidad',
        intro: "➕ Haz clic aquí para registrar una nueva comunidad.",
        position:'bottom'
        },
        ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Listo!',
        showStepNumbers: false
    })
    .start();
    }

function tourRegistrarComunidad() {
    introJs()
        .setOptions({
        steps: [
        { 
            intro: "🆕 Crea una nueva comunidad aquí."
        },
        {
        element: '#titulo-registrar-comunidad',
        intro: "📋 Aqui puedes registar todas tus comunidades",
        position: 'bottom'
        },
        {
        element: '#input-nombre-comunidad',
        intro: "✍️ Escribe aquí el nombre de tu nueva comunidad.",
        position: 'right'
        },
        {
        element: '#input-direccion-comunidad',
        intro: "✍️ Escribe aquí la direccion y comuna de tu nueva comunidad.",
        position: 'right'
        },
        {
        element: '#input-descripcion-comunidad',
        intro: "✍️ Añade una descripción detallada con las caracteristicas principales de tu comunidad.",
        position: 'right'
        },
        {
        element: '#btn-volver-comunidad',
        intro: "💾 Si necesitas informacion antes de guardar, pulsa aquí para volver listado comunidades.",
        position: 'bottom'
        },
        {
        element: '#btn-guardar-comunidad',
        intro: "💾 Cuando termines, pulsa aquí para guardar.",
        position: 'bottom'
        },
        
        ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Listo!',
        showStepNumbers: false
    })
    .start();
    }

function tourCrearSeguimiento() {
    // 1️⃣ recojo todos los elementos de la página
    const titleEl      = document.getElementById('titulo-crear-seguimiento');
    const docsEl       = document.getElementById('id_documentacion');   // el <select> o input que renderiza form.documentacion
    const existeEl     = document.getElementById('id_existe');          // el checkbox form.existe
    const obsEl        = document.getElementById('id_observaciones');   // el textarea form.observaciones
    const saveBtnEl    = document.getElementById('btn-guardar-seguimiento');
    const volverBtnEl    = document.getElementById('btn-volver-seguimiento');

    // 2️⃣ comprobación de existencia (para no romper si alguno falta)
    if (![titleEl, docsEl, existeEl, obsEl, saveBtnEl, volverBtnEl].every(el => el)) {
    return alert('⚠️ No pude encontrar todos los campos para el Tour Crear Seguimiento.');
    }

  // 3️⃣ lanzo Intro.js con esas referencias
    introJs()
        .setOptions({
        steps: [
        { 
            intro: "📄 Registra un nuevo seguimiento."
        },
        {
            element: titleEl,
            intro:   '📄 Título de la página: aquí empiezas tu nuevo seguimiento.',
            position:'bottom'
        },
        {
            element: docsEl,
            intro:   '📋 Selecciona el documento que vas a dar seguimiento.',
            position:'bottom'
        },
        {
            element: existeEl,
            intro:   '✅ Marca esta casilla si el documento ya está en tu poder.',
            position:'right'
        },
        {
            element: obsEl,
            intro:   '✍️ Añade aquí cualquier observación relevante.',
            position:'top'
        },
        {
            element: saveBtnEl,
            intro:   '💾 Cuando todo esté listo, pulsa aquí para guardar.',
            position:'bottom'
        },
        {
            element: volverBtnEl,
            intro: '🔙 Con este botón puedes volver al listado de Seguimiento Actualizado.',
            position: 'left'
        }
        ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Listo!',
        showStepNumbers:false,
        scrollToElement: true,
        overlayOpacity: 0.5
        })        
        .start();
    }

/**
 * Lanza el tour de Seguimiento "actualizado" o "pendiente"
 * @param {'actualizado'|'pendiente'} tipo
 */
function runTourSeguimiento(tipo) {
    // 0️⃣ Debug inicial
    console.log(`▶️ runTourSeguimiento(${tipo}) — URL:`, window.location.pathname);

    // 1️⃣ Localizamos los elementos (ahora sin buscar tour-ver-seguimiento-btn)
    const tourBtn = document.getElementById('btn-tutorial');
    const sufijo   = tipo === 'actualizado' ? '' : '-pendiente';
    const input    = document.getElementById(`input-buscar-seguimiento${sufijo}`);
    const btnB     = document.getElementById(`btn-buscar-seguimiento${sufijo}`);
    const btnR     = document.getElementById(`btn-reset-seguimiento${sufijo}`);
    const table    = document.getElementById('seguimientoTabla');
    const btnX     = document.getElementById(`btn-export-seguimiento${sufijo}-excel`);
    const btnP     = document.getElementById(`btn-export-seguimiento${sufijo}-pdf`);

  // ——— INICIO DEBUG —————————————————————————————————————————
    console.group(`Debug Tour ${tipo}`);
    console.log('tourBtn:', tourBtn);
    console.log('input:', input);
    console.log('btnBuscar:', btnB);
    console.log('btnReset:', btnR);
    console.log('tabla:', table);
    console.log('btnExcel:', btnX);
    console.log('btnPdf:', btnP);
    console.groupEnd();
  // ——— FIN DEBUG ——————————————————————————————————————————

    // 2️⃣ Verificamos que todos los elementos existan
    if (![tourBtn, input, btnB, btnR, table, btnX, btnP].every(el => el)) {
    return alert(`⚠️ No he podido encontrar todos los elementos para el Tour Seguimiento ${tipo}.`);
    }

     // 3️⃣ Arrancamos Intro.js
    introJs().setOptions({
    steps: [
        {
            element: tourBtn,
            intro: tipo === 'actualizado'
            ? '🔄 Gestiona tus seguimientos actualizados.'
            : '⏳ Gestiona tus seguimientos pendientes.'
        },
        {
        element: input,
        intro: '🔍 Busca por título de documento.',
        position: 'bottom'
        },
        {
        element: btnB,
        intro: '🖱️ Filtra los resultados.',
        position: 'right'
        },
        {
        element: btnR,
        intro: '🔄 Restablece el filtro.',
        position: 'right'
        },
        {
        element: table,
        intro: '🗂️ Aquí está la tabla con tus seguimientos.',
        position: 'top'
        },
        {
        element: btnX,
        intro: '📈 Aquí generas y descargas tu lista en Excel.',
        position: 'left'
        },
        {
        element: btnP,
        intro: '📄 Aquí generas y descargas tu lista en PDF.',
        position: 'bottom'
        }
    ],
    nextLabel: 'Siguiente',
    prevLabel: 'Anterior',
    doneLabel: '¡Listo!',
    showStepNumbers: false,
    scrollToElement: true,
    overlayOpacity: 0.5
    })
    .start();
}

function tourDashboardMantenimiento() {
    introJs().setOptions({
        steps: [
        { 
            intro: '🗓️ Panel de mantenimiento' 
        },
        {
            element: '#dashboard-title',
            intro: '🔧 Bienvenido al Dashboard de Mantenimiento: aquí tienes un vistazo general de todas tus mantenciones.',
            position: 'bottom'
        },
        {
            element: '#card-total-mantenciones',
            intro: '📊 Total de Mantenciones Anual: número total programado este año. Haz clic para detalles.',
            position: 'top'
        },
        {
            element: '#card-realizadas',
            intro: '✅ Mantenciones Realizadas: las ya completadas.',
            position: 'top'
        },
        {
            element: '#card-pendientes',
            intro: '⏳ Mantenciones Pendientes: aún por hacer.',
            position: 'top'
        },
        {
            element: '#card-instalaciones-pendientes',
            intro: '⚠️ Instalaciones con Mantenciones Pendientes: revisa estos puntos críticos.',
            position: 'top'
        },
        {
            element: '#metric-anual',
            intro: '📆 Mantenciones en el Año: programadas en 12 meses.',
            position: 'bottom'
        },
        {
            element: '#metric-mensual',
            intro: '🗓️ Mantenciones en el Mes: programadas en el mes actual.',
            placement: 'bottom'
        },
        {
            element: '#mantencionesChart',
            intro: '📈 Gráfico de Evolución: muestra tendencia mensual.',
            position: 'bottom'
        },
        {
            element: '#recent-title',
            intro: '📋 Últimas Mantenciones: estado y observaciones.',
            position: 'bottom'
        },
        {
            element: '#table-mantenciones-recientes',
            intro: '📑 Tabla de Mantenciones Recientes: detalles de cada registro.',
            position: 'top'
        }
        ],
            nextLabel: 'Siguiente',
            prevLabel: 'Anterior',
            doneLabel: '¡Entendido!',
            showStepNumbers: false,
        })
        .start();
        }

function tourMantencionesPreventivas() {
    const btnTutorial = document.getElementById('btn-tutorial');
    const tourItem    = document.getElementById('tour-mantencion-preventiva-btn');

    // 1️⃣ Validamos que estemos en la página correcta y tengamos el botón
    if (!btnTutorial) {
    return alert('⚠️ No encontré el botón de Tutorial.');
    }
    if (!/^\/mantenimiento\/comunidad\/\d+\/mantenciones\/?$/.test(window.location.pathname)) {
    return alert('⚠️ Ve primero a la página de Mantenciones Preventivas para este tour.');
    }

    // 2️⃣ Arrancamos Intro.js directamente
    introJs().setOptions({
    steps: [
        {
        element: '#btn-tutorial',
        intro:   '📖 Haz click aquí en “Tutorial” para relanzar este tour cuando quieras.',
        position:'bottom'
        },
        {
        element: '#mant-list-title',
        intro:   '📋 Aquí ves la Mantenciones Preventivas de la Comunidad.',
        position:'bottom'
        },
        {
        element: '#btn-nueva-mantencion',
        intro:   '➕ Pulsa aquí para crear una **nueva** mantención preventiva.',
        position:'right'
        },
        {
        element: '#filtro',
        intro:   '🔎 Usa este desplegable para filtrar según el estado.',
        position:'bottom'
        },
        {
        element: '#id_instalacion',
        intro: '🏭 Filtra por instalación concreta.',
        position: 'bottom'
        },
        {
        element: 'input[name="fecha_desde"]',
        intro: '📅 Selecciona la fecha “Desde...” para acotar tu búsqueda.',
        position: 'right'
        },
        {
        element: '#btn-filtrar',
        intro:   '🖱️ Aplica el filtro para ver solo las mantenciones que necesites.',
        position:'left'
        },
        {
        element: '#tabla-mantenciones',
        intro:   '📑 Esta es la tabla con todas tus mantenciones según el filtro.',
        position:'top'
        },
        {
        element: '#btn-editar-mantencion-tour',
        intro: '✏️ Usa este botón para actualizar la mantención preventiva.',
        position: 'right'
        },
        {
        element: 'a.btn-sm.btn-danger',
        intro: '🗑️ Y este elimina la mantención (cuidado: irreversible).',
        position: 'right'
        },
    ],
    nextLabel:      'Siguiente',
    prevLabel:      'Anterior',
    doneLabel:      '¡Entendido!',
    showStepNumbers:false,
    scrollToElement:true,
    overlayOpacity: 0.6
    }).start();
}

/**
 * Tour para el Tablero Kanban de Mantenimiento
 */
function tourKanban() {
    introJs().setOptions({
    steps: [
        {
        intro: '📊 Bienvenido al Tablero Kanban de Mantenimiento.'
        },
        {
        element: '#kanban-title',
        intro: '🏷️ Aquí está el título de la vista Kanban y la Comunidad.',
        position: 'bottom'
        },
        {
        element: '#col-pendientes',
        intro: '⏳ **Pendientes**: mantenciones programadas aún por hacer.',
        position: 'top'
        },
        {
        element: '#col-proceso',
        intro: '🔄 **En Proceso**: mantenciones que se estan ejecutando, esperando informe proveedor.',
        position: 'top'
        },
        {
        element: '#col-revision',
        intro: '🔍 **Revisión**: mantenciones a verificar previo informe proveedor, antes de cerrar.',
        position: 'top'
        },
        {
        element: '#col-completado',
        intro: '✅ **Completadas**: mantenciones aprobadas y terminadas.',
        position: 'top'
        },
        {
        element: '.kanban-card.card', // apunta a la primera tarjeta que encuentre
        intro: '✏️ Arrastra esta tarjeta para cambiarla de columna (estado).',
        position: 'right'
        }
    ],
    nextLabel: 'Siguiente',
    prevLabel: 'Anterior',
    doneLabel: '¡Entendido!',
    showStepNumbers: false,
    scrollToElement: true,
    overlayOpacity: 0.6
    }).start();
}

// ─── Función que define el tour de “Calendario de Mantenciones” ───────────────────
function tourCalendarioMantenciones() {
    // 1) Esperamos brevemente a que FullCalendar haya renderizado los botones
    //    (suele ser suficiente 300 ms, pero puedes ajustar si tu calendario tardara más)
    setTimeout(() => {
    introJs().setOptions({
        steps: [
        {
          // Paso 0: apuntar al botón “Tutorial”
            element: '#btn-tutorial',
            intro:   '🔄 Pulsa aquí para relanzar este Tour Calendario cuando quieras.',
            position:'bottom'
        },
        // Paso 1: el contenedor principal del calendario
        {
            element: '#calendar',
            intro:   '🗓️ Este es tu Calendario de Mantenciones: aquí ves todas las fechas programadas.',
            position:'top'
        },
        {
          // Paso 2: “Mes Anterior”
            element: '.fc-prev-button',
            intro:   '◀️ “Mes Anterior”: retrocede al mes previo.',
            position:'bottom'
        },
        {
          // Paso 3: “Mes Siguiente”
            element: '.fc-next-button',
            intro:   '▶️ “Mes Siguiente”: avanza al mes siguiente.',
            position:'bottom'
        },
        {
          // Paso 4: “Hoy”
            element: '.fc-today-button',
            intro:   '⏱️ Con “Hoy” vuelves al mes/semana actual.',
            position:'bottom'
        },
        {
          // Paso 5: “Mes” (vista de mes completo)
            element: '.fc-dayGridMonth-button',
            intro:   '🌄 “Mes” muestra todo el mes desplegado.',
            position:'bottom'
        },
        {
          // Paso 6: “Semana”
            element: '.fc-timeGridWeek-button',
            intro:   '📆 “Semana” muestra únicamente la semana en curso.',
            position:'bottom'
        },
        {
          // Paso 7: “Lista”
            element: '.fc-listWeek-button',
            intro:   '📋 “Lista” genera un listado de eventos de la semana.',
            position:'bottom'
        }
    ],
        nextLabel: 'Siguiente',
        prevLabel: 'Anterior',
        doneLabel: '¡Entendido!',
        showStepNumbers: false,
        scrollToElement: true,
        overlayOpacity: 0.6
    }).start();
    }, 300);
}

/**
 * Tour Informe de Mantenciones Preventivas
 * - Primera posición ancla al botón “📖 Tutorial” (id="btn-tutorial")
 * - Luego recorre filtros, tabla e íconos de DataTables.
 */
function tourInformeMantencion() {
    // 1) Mostrar un pequeño retraso en caso de que DataTables no haya renderizado aún sus botones
    setTimeout(() => {
    introJs().setOptions({
        steps: [
        {
            element: '#btn-tutorial',
            intro:   '🔄 Pulsa aquí para relanzar este Tour Informe cuando quieras.',
            position:'bottom'
        },
        {
            element: '#filterForm',
            intro:   '🔍 Usa estos filtros (Año / Mes) para acotar tu informe.',
            position:'bottom'
        },
        {
            element: '#btn-filtrar-informe',
            intro:   '🖱️ Luego pulsa “Filtrar” para aplicar esos criterios.',
            position:'bottom'
        },
        {
            element: '#informeTable',
            intro:   '📋 Aquí tienes la tabla con todos los datos de mantenciones.',
            position:'top'
        },
        {
            element: '.dt-buttons .buttons-excel',
            intro:   '📊 Exporta tus datos a Excel para analizarlos fuera del sistema.',
            position:'bottom'
        },
        {
            element: '.dt-buttons .buttons-pdf',
            intro:   '📄 Genera un PDF de este informe, listo para imprimir o compartir.',
            position:'bottom'
        },
        {
            element: '.dt-buttons .buttons-print',
            intro:   '🖨️ Imprime directamente desde aquí si lo necesitas en papel.',
            position:'bottom'
        }
    ],
        nextLabel:      'Siguiente',
        prevLabel:      'Anterior',
        doneLabel:      '¡Entendido!',
        showStepNumbers: false,
        scrollToElement: true,
        overlayOpacity: 0.6
    }).start();
}, 300);
}

/**
 * Tour para “Enviar Correo Individual”
 */
function tourCorreoIndividual() {
    // 1) Capturamos los elementos de la página
    const form         = document.getElementById('correo-form');
    const destinatario = document.querySelector('select[name="destinatario"]');
    const asunto       = document.querySelector('input[name="asunto"]');
    const mensaje      = document.querySelector('textarea[name="mensaje"]');
    const fileInput    = document.getElementById('file-input');
    const addFileBtn   = document.getElementById('add-file-btn');
    const fileList     = document.getElementById('file-list');
    const submitBtn    = document.querySelector('button[type="submit"]');

    // 2) Validamos que existan todos los elementos
    if (![form, destinatario, asunto, mensaje, fileInput, addFileBtn, fileList, submitBtn].every(el => el)) {
        return alert('⚠️ No he podido encontrar todos los elementos para el Tour Correo Individual.');
    }

    // 3) Arrancamos Intro.js
    introJs()
        .setOptions({
            steps: [
                {
                    // Mensaje inicial (sin elemento concreto)
                    intro: '📧 Bienvenido al formulario de “Enviar Correo Individual”.'
                },
                {
                    element: '#correo-form',
                    intro:   '🖋️ Este es el formulario para enviar un correo a un destinatario concreto.',
                    position:'top'
                },
                {
                    element: 'select[name="destinatario"]',
                    intro:   '👤 Aquí elige el destinatario al que deseas enviar el correo.',
                    position:'bottom'
                },
                {
                    element: 'input[name="asunto"]',
                    intro:   '✏️ Escribe el asunto de tu correo en este campo.',
                    position:'bottom'
                },
                {
                    element: 'textarea[name="mensaje"]',
                    intro:   '✍️ Redacta el cuerpo del mensaje que deseas enviar.',
                    position:'right'
                },
                {
                    element: '#file-input',
                    intro:   '📎 Selecciona el o los archivos que quieras adjuntar.',
                    position:'right'
                },
                {
                    element: '#add-file-btn',
                    intro:   '➕ Una vez elegido el archivo, pulsa aquí para añadirlo a la lista.',
                    position:'bottom'
                },
                {
                    element: '#file-list',
                    intro:   '📄 Aquí podrás ver el listado de archivos que has agregado.',
                    position:'top'
                },
                {
                    element: 'button[type="submit"]',
                    intro:   '🚀 Cuando estés listo, pulsa aquí para enviar el correo.',
                    position:'bottom'
                }
            ],
            nextLabel:      'Siguiente',
            prevLabel:      'Anterior',
            doneLabel:      '¡Listo!',
            showStepNumbers:false,
            scrollToElement:true,
            overlayOpacity:0.6
        })
        .start();
}

/**
 * Tour para “Enviar Correo Masivo”
 */
function tourCorreoMasivo() {
    // 1) Capturamos los elementos de la página
    const formMasc       = document.getElementById('correo-masivo-form');
    const checkboxes     = document.querySelectorAll('input[name="destinatarios"]');
    const asuntoMasc     = document.querySelector('input[name="asunto"]');
    const mensajeMasc    = document.querySelector('textarea[name="mensaje"]');
    const fileInputMasc  = document.getElementById('file-input');
    const addFileBtnMasc = document.getElementById('add-file-btn');
    const fileListMasc   = document.getElementById('file-list');
    const submitBtnMasc  = document.querySelector('#correo-masivo-form button[type="submit"]');

    // 2) Validamos que existan todos los elementos
    if (!formMasc ||
        checkboxes.length === 0 ||
        !asuntoMasc ||
        !mensajeMasc ||
        !fileInputMasc ||
        !addFileBtnMasc ||
        !fileListMasc ||
        !submitBtnMasc
    ) {
        return alert('⚠️ No he podido encontrar todos los elementos para el Tour Correo Masivo.');
    }

    // 3) Arrancamos Intro.js
    introJs()
        .setOptions({
            steps: [
                {
                    // Mensaje inicial
                    intro: '📧 Bienvenido al formulario de “Enviar Correo Masivo”.'
                },
                {
                    element: '#correo-masivo-form',
                    intro:   '🖋️ Este es el formulario completo para enviar correos a múltiples destinatarios.',
                    position:'top'
                },
                {
                    element: 'input[name="destinatarios"]',
                    intro:   '☑️ Marca uno o varios destinatarios de la lista.',
                    position:'bottom'
                },
                {
                    element: 'input[name="asunto"]',
                    intro:   '✏️ Escribe el asunto para los correos.',
                    position:'bottom'
                },
                {
                    element: 'textarea[name="mensaje"]',
                    intro:   '✍️ Redacta el mensaje que se enviará a todos los seleccionados.',
                    position:'right'
                },
                {
                    element: '#file-input',
                    intro:   '📎 Selecciona un archivo para adjuntar al correo masivo.',
                    position:'right'
                },
                {
                    element: '#add-file-btn',
                    intro:   '➕ Una vez elegido el archivo, pulsa aquí para añadirlo a la lista.',
                    position:'bottom'
                },
                {
                    element: '#file-list',
                    intro:   '📄 Aquí podrás ver todos los archivos que has agregado.',
                    position:'top'
                },
                {
                    element: 'button[type="submit"]',
                    intro:   '🚀 Cuando esté todo listo, pulsa aquí para enviar tu correo masivo.',
                    position:'bottom'
                }
            ],
            nextLabel:      'Siguiente',
            prevLabel:      'Anterior',
            doneLabel:      '¡Listo!',
            showStepNumbers:false,
            scrollToElement:true,
            overlayOpacity:0.6
        })
        .start();
}

/**
 * Tour para “Gestión de Destinatarios”
 */
function tourGestionarDestinatarios() {
    // 1) Capturar los elementos
    const encabezado     = document.querySelector('h2');
    const formAgregar    = document.querySelector('form');
    const btnGuardar     = formAgregar.querySelector('button[type="submit"]');
    const tabla          = document.querySelector('table.table');
    const editarPrimero  = document.querySelector('table.table tbody tr:first-child td:last-child a.btn-primary');
    const eliminarPrimero= document.querySelector('table.table tbody tr:first-child td:last-child a.btn-danger');

    // 2) Verificar que exista al menos el título y la tabla (los demás pueden estar vacíos si no hay registros)
    if (!encabezado || !formAgregar || !btnGuardar || !tabla) {
        return alert('⚠️ No he podido encontrar todos los elementos para el Tour Gestionar Destinatarios.');
    }

    // 3) Construir y arrancar Intro.js
    introJs()
        .setOptions({
            steps: [
                {
                    // Mensaje inicial:
                    intro: '👥 Bienvenido a la Gestión de Destinatarios de tu comunidad.'
                },
                {
                    element: 'h2',
                    intro:   '👤 Este es el encabezado de la sección “Gestión de Destinatarios”.',
                    position:'bottom'
                },
                {
                    element: 'form',
                    intro:   '✍️ Rellena este formulario para agregar un nuevo destinatario.',
                    position:'top'
                },
                {
                    element: 'button[type="submit"]',
                    intro:   '💾 Una vez completado, pulsa aquí para guardar el destinatario.',
                    position:'right'
                },
                {
                    element: 'h3, h2 + hr + h3', // si tu HTML usa un <hr> y luego <h3> “Lista de Destinatarios”
                    intro:   '📋 Aquí verás la lista de todos los destinatarios registrados.',
                    position:'bottom'
                },
                {
                    element: 'table.table tbody tr:first-child td:last-child a.btn-primary',
                    intro:   '✏️ Usa este botón para editar el primer destinatario de la lista.',
                    position:'left'
                },
                {
                    element: 'table.table tbody tr:first-child td:last-child a.btn-danger',
                    intro:   '🗑️ Usa este botón para eliminar el primer destinatario de la lista.',
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
        .start();
}

function tourBiblioteca() {
  // 0️⃣ Abrimos en primer lugar el desplegable “Tutorial” (para que Intro.js calcule posiciones)
    const tutorialButton = document.getElementById('btn-tutorial');
    if (!tutorialButton) {
        return alert("⚠️ No encontré el botón de Tutorial.");
    }
  // Aunque no haya un dropdown “tutorialesDropdown”, queremos destacar el botón “📖 Tutorial”:
  // No es obligatorio “mostrar” un dropdown, pero nos aseguramos de que exista.
  // (Si tuvieras un menú desplegable, aquí sería el lugar para abrirlo con bootstrap.Dropdown.getOrCreateInstance(...).show())

  // 1️⃣ Ejecutamos Intro.js con los pasos correspondientes:
    introJs().setOptions({
    steps: [
        {
        element: '#btn-tutorial',
        intro:   '📤 Pulsa aquí para relanzar el Tour Biblioteca en cualquier momento.',
        position:'bottom'
        },
        {
        element: 'a[title="Subir Archivo"]',
        intro:   '➕ Usa este botón para subir un nuevo archivo a la biblioteca.',
        position:'left'
        },
        {
        element: 'table.table',
        intro:   '📚 Aquí encontrarás la lista de todos los archivos disponibles.',
        position:'top'
        },
        {
        element: '.bi-download',
        intro:   '⬇️ Usa este icono para descargar el archivo directamente.',
        position:'auto'
        },
        {
        element: 'button.btn-danger',
        intro:   '🗑️ Pulsa este botón para eliminar un archivo de la biblioteca.',
        position:'auto'
        }
    ],
    nextLabel:      'Siguiente',
    prevLabel:      'Anterior',
    doneLabel:      '¡Entendido!',
    showStepNumbers:false,
    scrollToElement:true,
    overlayOpacity:0.6
    })
    .start();
}

/**
 * Tour para la pantalla “Subir Archivo” (URL: /biblioteca/<comunidad_id>/subir/)
 */
function tourSubirArchivo() {
  // 1️⃣ Destacar el botón único “Tutorial”
    const tutorialButton = document.getElementById('btn-tutorial');
    if (!tutorialButton) {
    return alert("⚠️ No encontré el botón de Tutorial.");
    }
  // (Optional) Si tuvieras un dropdown “tutorialesDropdown”, lo abrirías aquí.
  // Como ya usas sólo #btn-tutorial, con que exista nos basta.

  // 2️⃣ Configurar y lanzar Intro.js con los pasos
    introJs().setOptions({
    steps: [
        {
        element: '#btn-tutorial',
        intro:   '📤 Pulsa aquí para relanzar el Tour Subir Archivo cuando quieras.',
        position:'bottom'
        },
        {
        element: '#subir-archivo-title',
        intro:   '🗂️ Este es el título de la pantalla “Subir Archivo”.',
        position:'bottom'
        },
        {
        element: '#id_tipo',
        intro:   '🔖 Selecciona el <strong>Tipo</strong> al que pertenece este archivo.',
        position:'right'
        },
        {
        element: '#id_categoria',
        intro:   '📂 Elige la <strong>Categoría</strong> dentro de la que quedará registrado.',
        position:'right'
        },
        {
        element: '#id_titulo_documento',
        intro:   '✏️ Escribe un <strong>Título</strong> claro para tu documento.',
        position:'bottom'
        },
        {
        element: '#id_documento',
        intro:   '📎 Selecciona aquí el archivo que vas a subir desde tu ordenador.',
        position:'bottom'
        },
        {
        element: '#btn-subir-archivo',
        intro:   '🚀 Finalmente, haz clic en <strong>Subir Archivo</strong> para guardarlo.',
        position:'right'
        },
        {
        element: '#btn-volver-biblioteca',
        intro:   '🔙 Si necesitas regresar, pulsa aquí para volver a la Biblioteca.',
        position:'left'
        }
    ],
    nextLabel:      'Siguiente',
    prevLabel:      'Anterior',
    doneLabel:      '¡Listo!',
    showStepNumbers:false,
    scrollToElement:true,
    overlayOpacity: 0.6
    })
    .start();
}

/**
 * Tour “Contacto” (URL: /contacto/)
 */
function tourContacto() {
  // (Opcional) Mostrar un log para verificar que entramos en esta función
    console.log("▶️ tourContacto() arrancó");

  // 1️⃣ Asegurarnos de que exista el botón único “Tutorial”
    const tutorialButton = document.getElementById('btn-tutorial');
    if (!tutorialButton) {
        return alert("⚠️ No encontré el botón de Tutorial.");
    }

  // 2️⃣ Configurar y arrancar Intro.js
    introJs().setOptions({
    steps: [
        {
        element: '#btn-tutorial',
        intro:   '✉️ Pulsa aquí para relanzar el Tour de Contacto en cualquier momento.',
        position:'bottom'
        },
        {
        element: 'h1.text-center.my-4',
        intro:   '📬 Bienvenido a la página de Contacto: completa este formulario para enviarnos un mensaje.',
        position:'bottom'
        },
        {
        element: '#nombre',
        intro:   '👤 Aquí escribe tu nombre completo.',
        position:'right'
        },
        {
        element: '#email',
        intro:   '📧 Ingresa tu correo electrónico para que podamos responderte.',
        position:'right'
        },
        {
        element: '#mensaje',
        intro:   '💬 Redacta aquí tu mensaje o sugerencia.',
        position:'top'
        },
        {
        element: 'button[type="submit"]',
        intro:   '🚀 Finalmente, pulsa aquí para enviar tu mensaje al equipo de soporte.',
        position:'bottom'
        }
    ],
    nextLabel:      'Siguiente',
    prevLabel:      'Anterior',
    doneLabel:      '¡Enviado!',
    showStepNumbers: false,
    scrollToElement: true,
    overlayOpacity: 0.5
    }).start();
}

function tourCerrarSesion() {
    console.log("▶️ tourCerrarSesion() arrancó");

  // Paso A: comprobar existencia del botón de Tutorial
    const tutorialButton = document.getElementById('btn-tutorial');
    if (!tutorialButton) {
    return alert("⚠️ No encontré el botón de Tutorial.");
    }

  // Paso B: buscar el botón “Sí, cerrar sesión” dentro del form
  // (lo que renderiza logout_confirm.html)
    const logoutButton = document.querySelector('form button[type="submit"]');
    if (!logoutButton) {
    return alert("⚠️ No encontré el botón para cerrar sesión.");
    }

    // Paso C: buscar el enlace “Cancelar” que está junto al botón de cierre
    const cancelLink = document.querySelector('form a.btn-secondary');
    if (!cancelLink) {
        return alert("⚠️ No encontré el enlace para “Cancelar”.");
    }

    introJs().setOptions({
    steps: [
        {
        element: '#btn-tutorial',
        intro:   '🔰 Pulsa aquí para relanzar cualquier tour cuando quieras.',
        position:'bottom'
        },
        {
        element: logoutButton,
        intro:   '🔓 Pulsa aquí para confirmar “Cerrar Sesión”.',
        position:'bottom'
        },
        {
        element: cancelLink,
        intro:   '🚫 Pulsa aquí para cancelar y volver al listado de comunidades.',
        position:'bottom'
        }
        
    ],
    nextLabel: 'Siguiente',
    doneLabel: '¡Entendido!',
    showStepNumbers: false,
    scrollToElement: true,
    overlayOpacity: 0.5
    }).start();
}

