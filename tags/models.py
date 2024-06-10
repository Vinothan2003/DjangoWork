from django.db import models
# from store.models import Product
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=225)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    # what tag applied to what object

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type(product, video, image)
    # ID
    # product = models.ForeignKey(Product, on_delete=models.CASCADE) --> depended on store
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # -->GENERIC RELATIONSHIP
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()
