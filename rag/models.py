from django.db import models
from pgvector.django import VectorField
from django.contrib.postgres.fields import ArrayField


class DocumentChunk(models.Model):
    tenant_id = models.CharField(max_length=100)
    doc_type = models.CharField(max_length=100)
    source = models.CharField(max_length=255)
    content = models.TextField()
    embedding = VectorField(dimensions=768)
    effective_date = models.DateField(null=True)
    allowed_roles = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True
    )
    content_hash = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.doc_type} | {self.tenant_id}"