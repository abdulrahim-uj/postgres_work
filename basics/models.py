from django.db import models

import uuid
from django.db import models


# create a base model for handling re-usable fields
# fields that needed all models
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey("auth.User", blank=True,
                                related_name="creator_%(class)s_objects",
                                on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True,
                                related_name="updater_%(class)s_objects",
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
