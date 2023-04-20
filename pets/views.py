from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination
import ipdb


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        # QuerySet
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        # Validating input data:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # Same as below, but less verbose:
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        group = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not group:
            group = Group.objects.create(**group_data)

        pet_object = Pet.objects.create(
            **serializer.validated_data,
            group=group,
        )

        # OBS: traits_data is a list of dicts.
        for trait_dict in traits_data:
            trait = Trait.objects.filter(name__iexact=trait_dict["name"]).first()

            if not trait:
                # It's not possible to directly attribute a value to
                # a table in N:N relations. Therefore you need to use
                # .add() method.
                # In traits.models, the FK is called "pets", which
                # we need to reference so .add() method can work.
                trait = Trait.objects.create(**trait_dict)

            trait.pets.add(pet_object)

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
