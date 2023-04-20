from django.db import models


class Sex(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=Sex.choices, default=Sex.NOT_INFORMED)

    # And on the "Many" side of the relationship we add the FK:
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        related_name="pets",
    )

    def __repr__(self) -> str:
        return f"<Pet: ({self.id}) - name: {self.name} - age: {self.age} - weight: {self.weight} - sex: {self.sex}>"
