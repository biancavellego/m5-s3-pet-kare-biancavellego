from django.db import models

# Create your models here.
# pets
from django.db import models


class PetSex(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=PetSex.choices, default=PetSex.NOT_INFORMED
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.RESTRICT, related_name="pets", null=True
    )

    def __repr__(self) -> str:
        return f"<Pet: ({self.id}) - name: {self.name} - age: {self.age} - weight: {self.weight} - sex: {self.sex}>"
