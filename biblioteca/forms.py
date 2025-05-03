from django import forms
from django.core.exceptions import ValidationError
from .models import Archivo
from django.utils.safestring import mark_safe

class ArchivoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('Administracion', 'Administracion'),
        ('Contabilidad', 'Contabilidad'),
        ('Legal', 'Legal'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Personal', 'Personal'),
        ('Prevencion de Riesgos', 'Prevencion de Riesgos'),
        ('Seguridad', 'Seguridad'),
        ('Otros', 'Otros'),
    ]

    CATEGORIA_CHOICES = [
        ('Comunicacion', 'Comunicacion'),
        ('Comunidad', 'Comunidad'),
        ('Contable', 'Contable'),
        ('Gastos Comunes', 'Gastos Comunes'),
        ('Gestion de Emergencia', 'Gestion de Emergencia'),
        ('Inmobiliaria', 'Inmobiliaria'),
        ('Leyes Laborales', 'Leyes Laborales'),
        ('Libros', 'Libros'),
        ('Mantenimiento Preventivo', 'Mantenimiento Preventivo'),
        ('Manual', 'Manual'),
        ('Planos', 'Planos'),
        ('Proveedores', 'Proveedores'),
        ('Reglamentos', 'Reglamentos'),
        ('Resolucion de Conflictos', 'Resolucion de Conflictos'),
        ('Temas de Seguridad', 'Temas de Seguridad'),
        ('Otros', 'Otros'),
    ]

    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        label='Tipo', 
        widget=forms.Select(attrs={
        'class': 'form-select',
        'data-placeholder': 'Seleccione un tipo...'
        }),
        help_text=mark_safe("<i class='fa-solid fa-building'></i> Seleccione el tipo de área al que pertenece el archivo.")
        )
    
    categoria = forms.ChoiceField(
        choices=CATEGORIA_CHOICES, 
        label='Categoría',
        widget=forms.Select(attrs={
        'class': 'form-select',
        'data-placeholder': 'Seleccione una categoría...'
        }),
        help_text=mark_safe("<i class='fa-solid fa-list'></i> Seleccione la categoría que mejor describa el contenido del archivo. Debe estar en línea con el tipo seleccionado.")
    )
    
    class Meta:
        model = Archivo
        fields = ['tipo', 'categoria', 'titulo_documento', 'documento']
        exclude = ['comunidad']  # El campo comunidad se asignará en la vista
        
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        categoria = cleaned_data.get('categoria')

        # Ejemplo de validación: si el tipo es "Mantenimiento", se espera que la categoría sea "Mantenimiento Preventivo" u otra relacionada.
        if tipo == 'Mantenimiento' and categoria not in ['Mantenimiento Preventivo', 'Manual' 'Otros']:
            raise ValidationError("Para el tipo 'Mantenimiento', la categoría debe ser 'Mantenimiento Preventivo' o 'Otros'.")

        # Puedes agregar otras validaciones lógicas según tus necesidades.
        return cleaned_data
    