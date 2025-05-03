document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('tour-dashboard-mantenimiento-btn');
    if (!btn) return;

    btn.addEventListener('click', () => {
        const path = window.location.pathname;
        // /mantenimiento/comunidad/<id>/dashboard/
        if (!/^\/mantenimiento\/comunidad\/\d+\/dashboard\/$/.test(path)) {
            return alert('⚠️ Ve primero al Dashboard de Mantenimiento para este tour.');
        }
    
        introJs().setOptions({
            steps: [
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
            intro: '⚠️ Instalaciones con Pendientes: revisa estos puntos críticos.',
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
            element: '#mantencionesChart',
            intro: '📈 Gráfico de tendencia mensual.',
            position: 'top'
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
            scrollToElement: true,
            overlayOpacity: 0.6
        }).start();
        });
    });

