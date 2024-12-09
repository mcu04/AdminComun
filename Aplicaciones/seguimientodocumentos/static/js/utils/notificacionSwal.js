const notificacionSwal= (titleText, text, icon, confirmButtonText) => {
    
    Swal.fire({
        titleText: titleText,
        text: text,
        icon: icon,      // success, warning, error, info
        confirmButtonText: confirmButtonText
    });
};

