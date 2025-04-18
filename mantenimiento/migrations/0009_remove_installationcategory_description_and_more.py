# Generated by Django 5.1.4 on 2025-03-05 16:35

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0008_alter_instalacionpreventiva_mantencion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installationcategory',
            name='description',
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='costo',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Costo asociado a la mantención.', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='descripcion',
            field=models.TextField(blank=True, help_text='Descripción de la mantención preventiva.', null=True),
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='fecha_instalacion',
            field=models.DateField(default=datetime.date.today, help_text='Fecha de la instalación preventiva (usualmente la fecha programada).'),
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='mantencion',
            field=models.OneToOneField(help_text='Mantención preventiva asociada', on_delete=django.db.models.deletion.CASCADE, related_name='instalacion_preventiva', to='mantenimiento.mantencionpreventiva'),
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='observaciones',
            field=models.TextField(blank=True, help_text='Observaciones adicionales.', null=True),
        ),
        migrations.AlterField(
            model_name='instalacionpreventiva',
            name='responsable',
            field=models.ForeignKey(blank=True, help_text='Responsable de la mantención.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='installationcategory',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
