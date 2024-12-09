from django import forms
from .models import Archivo

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
        ('Planos', 'Planos'),
        ('Proveedores', 'Proveedores'),
        ('Reglamentos', 'Reglamentos'),
        ('Resolucion de Conflictos', 'Resolucion de Conflictos'),
        ('Temas de Seguridad', 'Temas de Seguridad'),
        ('Otros', 'Otros'),
    ]

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo', widget=forms.Select(attrs={'class': 'form-select'}))
    categoria = forms.ChoiceField(choices=CATEGORIA_CHOICES, label='Categoría', widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Archivo
        fields = ['tipo', 'categoria', 'titulo_documento', 'documento']