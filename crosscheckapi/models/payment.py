from django.db import models

class Payment(models.Model):
    amount = models.IntegerField()
    ref_num = models.CharField(max_length=100)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE)
    rented_property = models.ForeignKey("Property", on_delete=models.CASCADE)
    payment_type = models.ForeignKey("PaymentType", on_delete=models.CASCADE)