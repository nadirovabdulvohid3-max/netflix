from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validate_birthdate_limit(value):
    if value:
        min_date = date(1950,1, 1)
        if value <= min_date:
            raise ValidationError("Tug'ilgan sana 01.01.1950 dan katta bo'lishi kerak")

class Actor(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True, validators=[validate_birthdate_limit])
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.name  