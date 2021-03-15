from django.db import models

class Tenant(models.Model):
    phone_number = models.CharField(max_length=15, default=None, blank=True, null=True)
    email = models.CharField(max_length=150, default=None, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    landlord = models.ForeignKey("Landlord", on_delete=models.CASCADE)

    # @property
    # def full_name(self):
    #     "Returned the person's full name."
    #     return '%s %s' % (self.first_name, self.middle_initial, self.last_name)