from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
import ipdb


class PetView(APIView):
    def get(self, request: Request) -> Response:
        # QuerySet
        pets = Pet.objects.all()
        serializer = PetSerializer(instance=pets, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # Validating input data:
        serializer = PetSerializer(data=request.data)

        # request.data = {
        #     "name": "Strogonoff",
        #     "age": 4,
        #     "weight": 5,
        #     "sex": "Female",
        #     "group": {"scientific_name": "Felis catus"},
        #     "traits": [{"trait_name": "curious"}, {"trait_name": "hairy"}],
        # }

        # OBS: It's necessary to separate group and traits fields from the
        # dictionary in order to serialize them.

        serializer.is_valid(raise_exception=True)
        # Same as below, but less verbose:
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        pet_object = Pet.objects.create(**serializer.validated_data)
        Group.objects.create(**group_data, pet=pet_object)

        # Fazer for = traits é uma lista de dicts
        Trait.objects.create(**traits_data, pet=pet_object)

        # Formatting output object:
        serializer = PetSerializer(instance=pet_object)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        # OBS: serializer.validated_data is a dict.
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
