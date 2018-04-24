# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .actions import process_node_register_file, confirm_delete
from .tasks import bulk_whitelist, read_datajson
from .models import DatasetIndexingFile, NodeRegisterFile, Node, ReadDataJsonTask


class BaseRegisterFileAdmin(admin.ModelAdmin):
    actions = ['process_register_file']
    list_display = ('__unicode__', 'state', )
    readonly_fields = ('created', 'modified', 'state', 'logs')

    def process_register_file(self, _, queryset):
        raise NotImplementedError
    process_register_file.short_description = 'Ejecutar'

    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseRegisterFileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['uploader'].initial = request.user
        return form

    def save_form(self, request, form, change):
        return super(BaseRegisterFileAdmin, self).save_form(request, form, change)


class NodeRegisterFileAdmin(BaseRegisterFileAdmin):

    def process_register_file(self, _, queryset):
        for model in queryset:
            model.state = NodeRegisterFile.state = NodeRegisterFile.PROCESSING
            model.logs = u'-'
            model.save()
            process_node_register_file.delay(model)


class NodeAdmin(admin.ModelAdmin):

    list_display = ('catalog_id', 'indexable')
    actions = ('delete_model', 'run_indexing', 'make_indexable', 'make_unindexable')

    def get_actions(self, request):
        # Borro la acción de borrado default
        actions = super(NodeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def make_unindexable(self, _, queryset):
        queryset.update(indexable=False)
    make_unindexable.short_description = 'Marcar como no indexable'

    def make_indexable(self, _, queryset):
        queryset.update(indexable=True)
    make_indexable.short_description = 'Marcar como indexable'

    def delete_model(self, _, queryset):
        register_files = NodeRegisterFile.objects.all()
        for node in queryset:
            if node.indexable:
                confirm_delete(node, register_files)


class DataJsonAdmin(admin.ModelAdmin):
    readonly_fields = ('status', 'created', 'finished', 'logs', 'catalogs', 'stats')
    list_display = ('__unicode__', 'status')

    def save_model(self, request, obj, form, change):
        running_status = [ReadDataJsonTask.RUNNING, ReadDataJsonTask.INDEXING]
        if ReadDataJsonTask.objects.filter(status__in=running_status):
            return  # Ya hay tarea corriendo, no ejecuto una nueva
        super(DataJsonAdmin, self).save_model(request, obj, form, change)
        read_datajson.delay(obj)  # Ejecuta indexación


class DatasetIndexingFileAdmin(BaseRegisterFileAdmin):
    def process_register_file(self, _, queryset):
        for model in queryset:
            model.state = DatasetIndexingFile.state = DatasetIndexingFile.PROCESSING
            model.logs = u'-'  # Valor default mientras se ejecuta
            model.save()
            bulk_whitelist.delay(model.id)


admin.site.register(DatasetIndexingFile, DatasetIndexingFileAdmin)
admin.site.register(NodeRegisterFile, NodeRegisterFileAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(ReadDataJsonTask, DataJsonAdmin)
