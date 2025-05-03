from import_export.admin import ExportMixin
from django.contrib import admin
from .models import MantencionPreventiva
from .models import InstallationCategory

class MantencionPreventivaAdmin(ExportMixin, admin.ModelAdmin):
    pass

admin.site.register(MantencionPreventiva, MantencionPreventivaAdmin)


@admin.register(InstallationCategory)
class InstallationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']