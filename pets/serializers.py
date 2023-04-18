from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from pets.models import Sex


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Sex.choices, default=Sex.NOT_INFORMED)

    groups = GroupSerializer(read_only=True)
    traits = TraitSerializer(read_only=True, many=True)
