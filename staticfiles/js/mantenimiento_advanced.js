// Asegúrate de que jQuery ya esté cargado en la página

// Inicialización de DataTables en el informe de mantenciones

  $(document).ready(function() {
  initDataTables();
  initCalendar();
  initKanban();
  initNotifications();
  
});

// Esperamos a que el DOM esté cargado
$(document).ready(function() {
  // Si deseas también desactivar la configuración del formato de fecha, comenta la siguiente línea
  $.fn.dataTable.moment("DD/MM/YYYY");

  // Comenta la llamada a la función que inicializa DataTables
  // initDataTables();
});

/*
// Comenta (o elimina) toda la función initDataTables
function initDataTables() {
  const tableElement = $('#mantencionesTable');
  if (!tableElement.length) {
    return;
  }

  tableElement.DataTable({
    dom: 'lfrtip',
    order: [[1, 'asc'], [0, 'asc']],
    pageLength: 10,
    responsive: true,
    paging: true,
    ordering: true,
    info: true,
    language: {
      url: "{% static 'js/datatables_spanish.json' %}"
    }
  });
}
*/
/**
* Inicializa el calendario FullCalendar en el elemento #calendar.
* Se espera que el elemento tenga un atributo data-ajax-url con la URL de los eventos.
*/
function initCalendar() {
  const calendarElement = $('#calendar');
  if (!calendarElement.length) return;  // Si no existe el calendario, se detiene la función

  const calendar = new FullCalendar.Calendar(calendarElement[0], {
      locale: 'es', // Configuración para que se muestre en español
      initialView: 'dayGridMonth',
      headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,listWeek'
      },
       // Sobrescribe los textos de los botones para asegurar su traducción
      buttonText: {
        today: 'Hoy',
        month: 'Mes',
        week: 'Semana',
        day: 'Día',
        list: 'Lista'
    },
      events: calendarElement.data('ajax-url'),
      eventClick: function(info) {
          alert(`${info.event.title}\n${info.event.extendedProps.description || 'Sin descripción'}`);
      }
  });

  calendar.render();
}

$(document).ready(function() {
  
  console.log("Inicializando Kanban...");
  console.log("Elementos Kanban detectados:", $('.kanban-column').length);
  initKanban();
});

/**
* Inicializa el tablero Kanban en todas las columnas que tengan la clase .kanban-column.
* Cada columna debe tener definido el atributo data-update-url con la URL para actualizar el estado.
*/
function initKanban() {
  $('.kanban-column').each(function() {
      var updateUrl = $(this).data('update-url');
      if (!updateUrl) {
          console.warn("La columna no tiene 'data-update-url' definida:", this);
          return; // Si no hay URL, se omite esta columna
      }
      new Sortable(this, {
          group: 'kanban',      // Permite mover tarjetas entre columnas
          animation: 150,
          onEnd: function(evt) {
              var card = evt.item;
              var taskId = card.getAttribute('data-id');
              var newStatus = evt.to.getAttribute('data-status');
              
              if (!taskId || !newStatus) {
                  console.error("Error: taskId o newStatus no están definidos.");
                  return;
              }
              
              // Extraer la URL de actualización de la columna destino
              var url = $(evt.to).data('update-url');
              if (!url) {
                  console.error("Error: No se encontró 'data-update-url' en la columna destino.");
                  return;
              }
              
              // Enviar la actualización vía AJAX
              $.ajax({
                  url: url,
                  method: 'POST',
                  headers: { 'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val() },
                  data: JSON.stringify({ task_id: taskId, new_status: newStatus }),
                  contentType: 'application/json',
                  success: function(response) {
                      console.log("Estado actualizado correctamente:", response);
                  },
                  error: function(xhr, status, error) {
                      console.error("Error al actualizar el estado:", error);
                  }
              });
          }
      });
  });
}


/**
* Inicializa las notificaciones en tiempo real.
* Se muestra una notificación cada 30 segundos.
*/
function initNotifications() {
  setInterval(function() {
      showNotification("🔔 Recordatorio: Revisa las mantenciones programadas.");
  }, 30000);
}

/**
* Función para mostrar una notificación en la parte inferior de la pantalla.
* La notificación se elimina automáticamente después de 4 segundos.
* @param {string} message - El mensaje a mostrar.
*/
function showNotification(message) {
  const notif = $('<div class="notification"></div>').text(message);
  $('body').append(notif);
  notif.addClass('show');

  setTimeout(() => {
    notif.removeClass('show');
    setTimeout(() => notif.remove(), 500);
}, 4000);
}