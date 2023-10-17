from django.db import models
import uuid

class TokenIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['unique'] = True
        kwargs['default'] = uuid.uuid4
        super().__init__(*args, **kwargs)

class Role(models.Model):
    id = TokenIDField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'hospitalApi'
        db_table = 'role'
