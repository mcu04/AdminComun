$(document).ready(function () {
  console.log("Inicializando scripts...");

  // Inicializar DataTables si la tabla existe
  if ($("#mantencionesTable").length) {
    console.log("Tabla de mantenciones encontrada.");
    initDataTables();
  } else {
    console.warn("Tabla de mantenciones no encontrada, DataTables no se inicializa.");
  }

  // Inicializar FullCalendar si el contenedor existe
  if ($("#calendar").length) {
    console.log("Calendario encontrado.");
    initCalendar();
  } else {
    console.warn("Elemento del calendario no encontrado.");
  }

  // Inicializar Kanban si existen columnas Kanban
  if ($(".kanban-column").length) {
    console.log("Columnas Kanban encontradas.");
    initKanban();
  } else {
    console.warn("No hay columnas Kanban en la página.");
  }

  // Inicializar notificaciones (se puede activar en cualquier página)
  initNotifications();
});

///////////////////// FUNCIONES ///////////////////////

/**
 * Inicializa DataTables en la tabla de mantenciones.
 * Verifica la disponibilidad de DataTables y del plugin moment (para formatear fechas).
 */
function initDataTables() {
  const tableElement = $("#mantencionesTable");

  // Verificar si DataTables está cargado
  if (!$.fn.DataTable) {
    console.error("Error: DataTables no está cargado.");
    return;
  }

  // Si está disponible el plugin moment para DataTables, formatea las fechas
  if ($.fn.dataTable && $.fn.dataTable.moment) {
    $.fn.dataTable.moment("DD/MM/YYYY");
  } else {
    console.warn("Advertencia: el plugin 'moment' para DataTables no está disponible.");
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
 * Inicializa el calendario usando FullCalendar.
 * Se asegura de que el contenedor con id 'calendar' exista y que tenga asignada la URL de eventos a través de un atributo data-ajax-url.
 */
function initCalendar() {
  const calendarElement = $("#calendar")[0]; // Acceder al elemento nativo
  if (!calendarElement) return;

  const calendar = new FullCalendar.Calendar(calendarElement, {
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
    // Se espera que el contenedor tenga el atributo data-ajax-url
    events: $("#calendar").data("ajax-url"),
    eventClick: function (info) {
      alert(`${info.event.title}\n${info.event.extendedProps.description || "Sin descripción"}`);
    },
  });

  calendar.render();
  console.log("Calendario inicializado correctamente.");
}

/**
 * Inicializa el tablero Kanban usando SortableJS.
 * Recorre cada elemento con la clase .kanban-column y añade la funcionalidad para mover tarjetas.
 */
function initKanban() {
  $(".kanban-column").each(function () {
    var updateUrl = $(this).data("update-url");
    if (!updateUrl) {
      console.warn("La columna Kanban no tiene 'data-update-url' definida.", this);
      return;
    }

    new Sortable(this, {
      group: "kanban", // Permite mover tarjetas entre columnas
      animation: 150,
      onEnd: function (evt) {
        const card = evt.item;
        const taskId = card.getAttribute("data-id");
        const newStatus = evt.to.getAttribute("data-status");

        if (!taskId || !newStatus) {
          console.error("Error: taskId o newStatus no están definidos.");
          return;
        }

        // Realiza la actualización mediante AJAX
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
 * Inicializa las notificaciones.
 */
function initNotifications() {
  console.log("Notificaciones inicializadas.");
}

/**
 * Muestra una notificación temporal en pantalla.
 * @param {string} message - El mensaje a mostrar.
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






















