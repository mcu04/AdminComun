from django import forms

class MultiFileInput(forms.ClearableFileInput):
    # Permite la selección múltiple en el navegador
    allow_multiple_selected = True
    
    def value_from_datadict(self, data, files, name):
        """
        Devuelve una lista de archivos para el campo, en lugar de uno solo.
        """
        return files.getlist(name)


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    
    def to_python(self, data):
        """
        Convierte los datos en una lista de archivos.
        Si no hay datos, devuelve una lista vacía.
        """
        if not data:
            return []
        
        # Si data ya es una lista (como ocurre cuando se envían múltiples archivos)
        if isinstance(data, list):
            return data
        return [data]

    def validate(self, data):
        """
        Valida que si el campo es requerido, se suba al menos un archivo.
        """
        if self.required and not data:
            raise forms.ValidationError("Debes seleccionar al menos un archivo.")
        # Llama a la validación estándar para cada archivo individual (opcional)
        for f in data:
            super(MultiFileField, self).validate(f)