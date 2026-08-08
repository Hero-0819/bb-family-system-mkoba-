from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),

        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(),
        ),

        migrations.CreateModel(
            name='PaymentAllocation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    ),
                ),
                (
                    'contribution_month',
                    models.PositiveSmallIntegerField(),
                ),
                (
                    'contribution_year',
                    models.PositiveIntegerField(),
                ),
                (
                    'amount_allocated',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                    ),
                ),
                (
                    'payment',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='allocations',
                        to='payments.payment',
                    ),
                ),
            ],
            options={
                'ordering': [
                    'contribution_year',
                    'contribution_month',
                ],
            },
        ),
    ]
