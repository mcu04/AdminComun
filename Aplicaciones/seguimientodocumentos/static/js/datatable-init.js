$(document).ready(function () {
    $('#seguimientoTabla').DataTable({
        language: {
            url: "{% static 'js/datatables_spanish.json' %}",
        },
        responsive: true,
        pageLength: 10,
        paging: true,
        ordering: true,
        info: true,
    });
});