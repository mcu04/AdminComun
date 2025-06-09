from django import forms
from django.core.exceptions import ValidationError
from .models import Archivo, TipoDocumento, CategoriaDocumento
from django.utils.safestring import mark_safe

class ArchivoForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all().order_by("nombre"),
        label="Tipo",
        widget=forms.Select(attrs={
            "class": "form-select",
            "data-placeholder": "Seleccione un tipo..."
        }),
        help_text=mark_safe("<i class='fa-solid fa-building'></i> Seleccione el tipo de área al que pertenece el archivo.")
    )
    
    categoria = forms.ModelChoiceField(
        queryset=CategoriaDocumento.objects.none(),  # inicialmente vacío; veremos más abajo cómo filtrar por tipo
        label="Categoría",
        widget=forms.Select(attrs={
            "class": "form-select",
            "data-placeholder": "Seleccione una categoría..."
        }),
        help_text=mark_safe("<i class='fa-solid fa-list'></i> Seleccione la categoría que mejor describa el contenido del archivo.")
    )
    
    class Meta:
        model = Archivo
        fields = ['tipo', 'categoria', 'titulo_documento', 'documento']
        exclude = ['comunidad']  # El campo comunidad se asignará en la vista
        
    def __init__(self, *args, **kwargs):
        """
        Sobrescribimos el __init__ para, si llega un 'tipo' en data/initial,
        rellenar solo las categorías asociadas a ese tipo.
        """
        super().__init__(*args, **kwargs)

        # 1) Si el formulario viene de POST (o initial) con un valor para 'tipo',
        #    cargamos solo las categorías que correspondan a ese TipoDocumento.
        if "tipo" in self.data:
            try:
                tipo_id = int(self.data.get("tipo"))
                self.fields["categoria"].queryset = CategoriaDocumento.objects.filter(
                    tipo_id=tipo_id
                ).order_by("nombre")
            except (ValueError, TypeError):
                # si no viene un entero válido, dejamos queryset vacío
                self.fields["categoria"].queryset = CategoriaDocumento.objects.none()

        # 2) Si el formulario ya tiene un instance (edición),
        #    preseleccionamos las categorías de ese tipo.
        elif self.instance and self.instance.pk:
            tipo_obj = self.instance.tipo
            if tipo_obj:
                self.fields["categoria"].queryset = CategoriaDocumento.objects.filter(
                    tipo=tipo_obj
                ).order_by("nombre")
            else:
                self.fields["categoria"].queryset = CategoriaDocumento.objects.none()
        else:
            # por defecto no mostramos ninguna categoría hasta que el usuario elija el tipo
            self.fields["categoria"].queryset = CategoriaDocumento.objects.none()
    