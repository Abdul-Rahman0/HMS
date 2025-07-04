# Generated by Django 4.2.10 on 2025-06-13 19:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_hostelcertificate_certificate_number_and_more'),
        ('payments', '0002_alter_payment_payment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrefund',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='paymentrefund',
            name='processed_by',
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='receipt_number',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.CharField(blank=True, choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.studentprofile'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('failed', 'Failed'), ('pending', 'Pending')], max_length=10),
        ),
        migrations.DeleteModel(
            name='PaymentReceipt',
        ),
        migrations.DeleteModel(
            name='PaymentRefund',
        ),
    ]
