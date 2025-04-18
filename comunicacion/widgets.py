from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    # Permite seleccionar múltiples archivos
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        return files.getlist(name)