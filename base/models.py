import uuid

from django.db import models


# Create your models here.


class CreateUpdateDate(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class UniqueIds(models.Model):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True, unique=True)
    #  public id to share with the in url,
    #  Used for REST routes and public displays
    public_id = models.BigIntegerField(editable=False, unique=True)


class PublicId:
    # method for generating public id
    @staticmethod
    def create_public_id():
        public_id = uuid.uuid4().int >> 75
        return public_id


class BaseModel(CreateUpdateDate, UniqueIds):
    """
    Create model for inheriting purpose only.
    """

    class Meta:
        abstract = True

    pass
