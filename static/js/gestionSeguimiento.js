/*
const $formularioSeguimiento = document.getElementById('formularioSeguimiento');
const $txtexiste = document.getElementById('txtexiste');
const btnsEliminacion =document.querySelectorAll('.btnEliminacion');

(function (){

    notificacionSwal(document.title, "Seguimiento registrado con exito", "success", "ok")

    formularioSeguimiento.addEventListener('submit', function(e) {
        let existe = String(existe.value).trim();
        if (existe.length < 3) {
            notificacionSwal= (document.title, "El campo existe no puede estar vacio", "warning", "ok")
            e.preventDefault();
        }
    });

    btnsEliminacion.forEach(btn => {
        btn.addEventListener('click', function (e) {
            let confirmacion = confirm('¿Confirmar la eliminacion del Seguimiento?')
            if (!confirmacion) {
                e.preventDefault();
            }
        })
    })

})();


    btnsEliminacion.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            Swal.fire({
                title: "¿Confirma la eliminación del seguimiento?",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor: "#d33",
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    location.href = e.target.href
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,
            });
        });
    });
        
})();

// Obteniendo elementos del DOM    AI
// Validando antes de enviar
//$formularioSeguimiento.addEventListener('submit', function(e) {

    // Si el campo "txtexiste" está vacío, prevenir el envío
   // if (!$txtexiste || $txtexiste.value.trim() === '') {
       // e.preventDefault();
       // alert("El campo 'txtexiste' no puede estar vacío.");
    //} else {
        //alert("Formulario válido, puedes enviarlo.");
   // }
//});
*/

document.addEventListener('DOMContentLoaded', function () {
    const formularioSeguimiento = document.getElementById('formularioSeguimiento');
    const existe = document.getElementById('txtexiste');
    const btnsEliminacion = document.querySelectorAll('.btnEliminacion');

/*    const notificacionSwal = (titleText, text, icon, confirmButtonText) => {
        Swal.fire({
            titleText: titleText,
            text: text,
            icon: icon, // success, warning, error, info
            confirmButtonText: confirmButtonText,
        });
    };
*/
    // Alerta de seguimiento registrado con éxito
    notificacionSwal(document.title, "Seguimiento registrado con éxito", "success", "Ok");

    // Validación del formulario
    formularioSeguimiento.addEventListener('submit', function (e) {
        const existeValue = String(existe.value).trim();
        if (existeValue.length < 3) {
            notificacionSwal(
                document.title,
                "El campo 'Existe' no puede estar vacío o tener menos de 3 caracteres",
                "warning",
                "Ok"
            );
            e.preventDefault();
        }
    });

    // Confirmación antes de eliminar
    btnsEliminacion.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // Evita la acción predeterminada del botón
            Swal.fire({
                title: "¿Confirma la eliminación del seguimiento?",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor: "#d33",
                cancelButtonText: "Cancelar",
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    // Si el botón está en un enlace, usa href para redirigir
                    const href = e.target.getAttribute('href');
                    if (href) {
                        window.location.href = href;
                    }
                },
                allowOutsideClick: false,
                allowEscapeKey: false,
            });
        });
    });
});