from django.db import models

from common.models import Timestamped


class Organization(Timestamped):
    inn = models.CharField(
        max_length=12,
        verbose_name='ИНН организации',
        primary_key=True,
        editable=False,
    )
    balance = models.PositiveIntegerField(
        verbose_name='Баланс'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['inn']

    def __str__(self):
        return f'Организация {self.inn}'


class PaymentLogs(Timestamped):
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.PROTECT,
        verbose_name='Организация',
        related_name='payment_logs',
    )
    payment = models.ForeignKey(
        'operations.Payment',
        on_delete=models.PROTECT,
        verbose_name='Платежный документ',
        related_name='logs',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма'
    )
    organization_balance_before = models.PositiveIntegerField(
        verbose_name='Баланс до изменения'
    )
    organization_balance_after = models.PositiveIntegerField(
        verbose_name='Баланс после изменения'
    )

    class Meta:
        verbose_name = 'Лог платежа'
        verbose_name_plural = 'Логи платежей'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['payment']),
        ]

    def __str__(self):
        return (f"Лог платежа {self.payment} для {self.organization} на сумму {self.amount}")
