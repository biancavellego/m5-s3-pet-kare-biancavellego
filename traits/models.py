from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    pets = models.ManyToManyField(
        # Referenced model file location:
        "pets.Pet",
        # ManyToMany does not require on_delete field, it's always CASCADE.
        related_name="traits",
    )

    def __repr__(self) -> str:
        return (
            f"<Trait: ({self.id}) - name: {self.name}- created_at: {self.created_at}>"
        )
