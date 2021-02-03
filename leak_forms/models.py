from django.db import models

class LeakevidenceModel(models.Model):
    files = models.FileField(upload_to='', blank=False, default = None)

    class Meta:
        ordering = ['files']