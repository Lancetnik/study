from django.db import models


class FakeDeletionMixin:
    def delete(self, *args, **kwargs):
        self.update(is_deleted=True)


class FakeDeletionQueryset(FakeDeletionMixin, models.QuerySet):
    pass


class FakeDeletionModel(models.Model):
    objects = FakeDeletionQueryset.as_manager()

    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    class Meta:
        abstract = True
