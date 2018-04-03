#! coding: utf-8

from django.utils import timezone
from django_rq import job

from django_datajsonar.apps.management.actions import DatasetIndexableToggler
from django_datajsonar.apps.management.models import Node, DatasetIndexingFile
from django_datajsonar.apps.management.strings import FILE_READ_ERROR
from django_datajsonar.libs.indexing.catalog_reader import index_catalog


@job('indexing')
def read_datajson(task, whitelist=False, read_local=False):
    """Tarea raíz de indexación. Itera sobre todos los nodos indexables (federados) e
    inicia la tarea de indexación sobre cada uno de ellos
    """
    nodes = Node.objects.filter(indexable=True)
    for node in nodes:
        index_catalog(node, task, read_local, whitelist)


@job('indexing')
def bulk_whitelist(indexing_file_id):
    """Marca datasets como indexables en conjunto a partir de la lectura
    del archivo la instancia del DatasetIndexingFile pasado
    """
    indexing_file_model = DatasetIndexingFile.objects.get(id=indexing_file_id)
    toggler = DatasetIndexableToggler()
    try:
        logs_list = toggler.process(indexing_file_model.indexing_file)
        logs = ''
        for log in logs_list:
            logs += log + '\n'

        state = DatasetIndexingFile.PROCESSED
    except ValueError:
        logs = FILE_READ_ERROR
        state = DatasetIndexingFile.FAILED

    indexing_file_model.state = state
    indexing_file_model.logs = logs
    indexing_file_model.modified = timezone.now()
    indexing_file_model.save()
