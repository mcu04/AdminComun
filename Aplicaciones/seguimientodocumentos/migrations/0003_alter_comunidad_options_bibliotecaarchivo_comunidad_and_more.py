# Generated by Django 5.1.4 on 2024-12-23 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimientodocumentos', '0002_comunidad_descripcion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comunidad',
            options={'ordering': ['nombre'], 'verbose_name': 'Comunidad', 'verbose_name_plural': 'Comunidades'},
        ),
        migrations.AddField(
            model_name='bibliotecaarchivo',
            name='comunidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seguimientodocumentos.comunidad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='comunidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seguimientodocumentos.comunidad'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='direccion',
            field=models.CharField(max_length=200, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre de la Comunidad'),
        ),
        migrations.AlterField(
            model_name='documentacion',
            name='comunidad',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seguimiento_documentos', to='seguimientodocumentos.comunidad', verbose_name='Comunidad'),
        ),
        migrations.AlterUniqueTogether(
            name='comunidad',
            unique_together={('nombre', 'direccion')},
        ),
    ]
