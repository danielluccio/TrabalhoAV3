# controle/models.py

from django.db import models
import math


M = 0.13



FAIXAS_CE = [
    ('SAN', 'SBV'),
    ('RIA', 'RIN'),
    ('PMA', 'POZ'),
    ('OZA', 'OZA'),
    ('ORN', 'OSV'),
    ('OHX', 'OIQ'),
    ('OCB', 'OCU'),
    ('NUM', 'NVF'),
    ('NQL', 'NRE'),
    ('HTX', 'HZA')
]

FAIXAS_MA = [
    ('HOL', 'HQE'),
    ('NHA', 'NHT'),
    ('NMP', 'NNI'),
    ('NWS', 'NXQ'),
    ('OIR', 'OJQ'),
    ('OXQ', 'OXZ'),
    ('PSA', 'PTZ'),
    ('ROA', 'ROZ')
]

FAIXAS_PI = [
    ('LVF', 'LWQ'),
    ('NHU', 'NIX'),
    ('ODU', 'OEI'),
    ('OUA', 'OUE'),
    ('OVW', 'OVY'),
    ('PIA', 'PIZ'),
    ('QRN', 'QRZ'),
    ('RSG', 'RST')
]


def prefixo_in_faixa(prefixo, inicio, fim):
    return inicio <= prefixo <= fim

class RegistroEstacionamento(models.Model):
    placa = models.CharField(max_length=7)
    estado = models.CharField(max_length=50, blank=True)
    entrada = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    valor_pago = models.FloatField(blank=True, null=True)

    def identificar_estado(self):
        prefixo = self.placa[:3].upper()

        
        for inicio, fim in FAIXAS_CE:
            if prefixo_in_faixa(prefixo, inicio, fim):
                return 'Ceará'


        for inicio, fim in FAIXAS_MA:
            if prefixo_in_faixa(prefixo, inicio, fim):
                return 'Maranhão'

       
        for inicio, fim in FAIXAS_PI:
            if prefixo_in_faixa(prefixo, inicio, fim):
                return 'Piauí'

       
        return 'Outro estado'

    def calcular_valor(self):
        if not self.entrada or not self.saida:
            return None 

        tempo_total = (self.saida - self.entrada).total_seconds() / 60 

        if tempo_total <= 15:
            return 0.0

        tempo_cobravel = tempo_total - 15

        if tempo_cobravel <= 180:
            return 10.0
        else:
            valor = 10.0
            tempo_extra = tempo_cobravel - 180
            blocos_20_min = math.ceil(tempo_extra / 20)
            valor_extra = blocos_20_min * (2 + M)
            return valor + valor_extra

    def save(self, *args, **kwargs):
        self.estado = self.identificar_estado()
        self.valor_pago = self.calcular_valor()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.placa} ({self.estado}) - Valor: R$ {self.valor_pago if self.valor_pago is not None else 'N/A'}"
