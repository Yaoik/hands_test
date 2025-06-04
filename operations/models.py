from django.db import models

from common.models import Timestamped


class Payment(Timestamped):
    operation_id = models.UUIDField(
        primary_key=True,
        verbose_name='ID операции'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма'
    )
    payer_inn = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        verbose_name='ИНН плательщика'
    )
    document_number = models.CharField(
        max_length=50,
        verbose_name='Номер документа'
    )
    document_date = models.DateTimeField(
        verbose_name='Дата документа'
    )

    class Meta:
        verbose_name = 'Платежный документ'
        verbose_name_plural = 'Платежные документы'
        ordering = ['-document_date']

    def __str__(self):
        return f'{self.document_number} от {self.document_date.date()} на сумму {self.amount}'
