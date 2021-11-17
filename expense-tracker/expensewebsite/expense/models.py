from django.db import models
from django.utils.timezone import now

# Create your models here.
class Expense(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
