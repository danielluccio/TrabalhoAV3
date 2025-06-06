from django.contrib import admin
from .models import RegistroEstacionamento

@admin.register(RegistroEstacionamento)
class RegistroEstacionamentoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'estado', 'entrada', 'saida', 'valor_pago')
    readonly_fields = ('estado', 'valor_pago')
