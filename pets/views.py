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

        # full_pet_data = {
        #     "name": "Strogonoff",
        #     "age": 4,
        #     "weight": 5,
        #     "sex": "Female",
        #     "group": {"scientific_name": "Felis catus"},
        #     "traits": [{"trait_name": "curious"}, {"trait_name": "hairy"}],
        # }

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        print(serializer.validated_data)

        # group_data = serializer.validated_data.pop("groups")
        # traits_data = serializer.validated_data.pop("traits")
        pet_object = Pet.objects.create(**serializer.validated_data)
        # Group.objects.create(**group_data, pet=pet_object)
        # Trait.objects.create(**traits_data, pet=pet_object)

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
        serializer = PetSerializer(instance=pet)

        return Response({"message": "patch id route"}, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(status.HTTP_204_NO_CONTENT)
