from import_export.admin import ExportMixin
from django.contrib import admin
from .models import MantencionPreventiva

class MantencionPreventivaAdmin(ExportMixin, admin.ModelAdmin):
    pass

admin.site.register(MantencionPreventiva, MantencionPreventivaAdmin)
