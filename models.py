# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Seguimiento(models.Model):
    id = models.BigAutoField(primary_key=True)
    existe = models.CharField(max_length=10)
    fecha_registrado = models.DateField()
    fecha_actualizado = models.DateField(blank=True, null=True)
    observaciones = models.CharField(max_length=200, blank=True, null=True)
    documentacion = models.ForeignKey('SeguimientodocumentosDocumentacion', models.DO_NOTHING, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    titulo_documento = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seguimiento'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BibliotecaArchivo(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    titulo_documento = models.CharField(max_length=255)
    documento = models.CharField(max_length=100)
    fecha_subida = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'biblioteca_archivo'


class BibliotecaDocumento(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=10)
    fecha_subida = models.DateTimeField()
    estado = models.CharField(max_length=50)
    fecha_descarga = models.DateTimeField(blank=True, null=True)
    url_origen = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblioteca_documento'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Prueba(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prueba'


class SeguimientodocumentosDocumentacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    titulo_documento = models.CharField(max_length=200)
    comunidad = models.ForeignKey('SeguimientodocumentosComunidad', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientodocumentos_Documentacion'


class SeguimientodocumentosComunidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    administrador = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'seguimientodocumentos_comunidad'
