$(document).ready(function () {
  console.log("Inicializando scripts...");

  // Inicializar DataTables solo si la tabla existe en el DOM
  if ($("#mantencionesTable").length) {
      initDataTables();
  } else {
      console.warn("Tabla de mantenciones no encontrada, DataTables no se inicializa.");
  }

  // Inicializar FullCalendar si el elemento existe
  if ($("#calendar").length) {
      initCalendar();
  } else {
      console.warn("Elemento del calendario no encontrado.");
  }

  // Inicializar Kanban solo si hay elementos .kanban-column
  if ($(".kanban-column").length) {
      initKanban();
  } else {
      console.warn("No hay columnas Kanban en la página.");
  }

  // Notificaciones listas
  initNotifications();
});

/**
* Inicializa DataTables con configuración en español
*/
function initDataTables() {
  console.log("Inicializando DataTables...");

  const tableElement = $("#mantencionesTable");
  if (!tableElement.length) return;

  // Verificar si $.fn.dataTable está disponible
  if (!$.fn.DataTable) {
      console.error("Error: DataTables no está cargado.");
      return;
  }

  // Verificar si el plugin moment para DataTables está disponible
  if (!$.fn.dataTable.moment) {
      console.warn("Advertencia: el plugin 'moment' para DataTables no está disponible.");
  } else {
      $.fn.dataTable.moment("DD/MM/YYYY");
  }

  tableElement.DataTable({
      dom: "lfrtip",
      order: [[1, "asc"], [0, "asc"]],
      pageLength: 10,
      responsive: true,
      paging: true,
      ordering: true,
      info: true,
      language: {
          url: "/static/js/datatables_spanish.json",
      },
  });

  console.log("DataTables inicializado correctamente.");
}

/**
* Inicializa el calendario con FullCalendar
*/
function initCalendar() {
  console.log("Inicializando FullCalendar...");

  const calendarElement = $("#calendar");
  if (!calendarElement.length) return;

  const calendar = new FullCalendar.Calendar(calendarElement[0], {
      locale: "es",
      initialView: "dayGridMonth",
      headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,listWeek",
      },
      buttonText: {
          today: "Hoy",
          month: "Mes",
          week: "Semana",
          day: "Día",
          list: "Lista",
      },
      events: calendarElement.data("ajax-url"),
      eventClick: function (info) {
          alert(`${info.event.title}\n${info.event.extendedProps.description || "Sin descripción"}`);
      },
  });

  calendar.render();
  console.log("Calendario inicializado correctamente.");
}

/**
* Inicializa Kanban con SortableJS
*/
function initKanban() {
  console.log("Inicializando Kanban...");

  $(".kanban-column").each(function () {
      var updateUrl = $(this).data("update-url");
      if (!updateUrl) {
          console.warn("La columna Kanban no tiene 'data-update-url' definida.");
          return;
      }

      new Sortable(this, {
          group: "kanban",
          animation: 150,
          onEnd: function (evt) {
              var card = evt.item;
              var taskId = card.getAttribute("data-id");
              var newStatus = evt.to.getAttribute("data-status");

              if (!taskId || !newStatus) {
                  console.error("Error: taskId o newStatus no están definidos.");
                  return;
              }

              // Enviar actualización vía AJAX
              $.ajax({
                  url: updateUrl,
                  method: "POST",
                  headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                  data: JSON.stringify({ task_id: taskId, new_status: newStatus }),
                  contentType: "application/json",
                  success: function (response) {
                      console.log("Estado actualizado correctamente:", response);
                  },
                  error: function (xhr, status, error) {
                      console.error("Error al actualizar el estado:", error);
                  },
              });
          },
      });
  });

  console.log("Kanban inicializado correctamente.");
}

/**
* Inicializa las notificaciones en la aplicación
*/
function initNotifications() {
  console.log("Notificaciones inicializadas.");
}

/**
* Muestra una notificación con un mensaje específico.
* @param {string} message - Mensaje a mostrar.
*/
function showNotification(message) {
  const notif = $('<div class="notification"></div>').text(message);
  $("body").append(notif);
  notif.addClass("show");

  setTimeout(() => {
      notif.removeClass("show");
      setTimeout(() => notif.remove(), 500);
  }, 4000);
}










 










