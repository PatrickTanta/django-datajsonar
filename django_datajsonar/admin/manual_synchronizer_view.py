from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from django_datajsonar.forms.manual_synchronizer_form import ManualSynchronizerRunForm
from django_datajsonar.models import Synchronizer, Node


class ManualSynchronizerView(View):
    def get(self, request, synchro_id):
        synchro = Synchronizer.objects.get(id=synchro_id)
        context = {
            'opts': Synchronizer._meta,
            'has_change_permission': True,
            'form': ManualSynchronizerRunForm(),
            'object': synchro,
        }
        return render(request, 'synchronizer_manual_run.html', context=context)

    def post(self, request, synchro_id):
        synchro = Synchronizer.objects.get(id=synchro_id)
        try:
            synchro.node = Node.objects.get(id=request.POST.get('node'))
            synchro.begin_stage()
            messages.success(request, "Corriendo tarea!")
        except Exception:
            messages.error(request, "El synchronizer seleccionado ya está corriendo")
        return redirect('admin:django_datajsonar_synchronizer_changelist')
