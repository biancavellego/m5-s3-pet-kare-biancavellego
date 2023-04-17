from django.db import models

# Create your models here.
# groups
from django.db import models


class Group(models.Model):
    scientific_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=False, null=True)

    def __repr__(self) -> str:
        return f"<Group: ({self.id}) - name: {self.scientific_name} - created_at: {self.created_at}>"
