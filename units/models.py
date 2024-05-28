from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
