from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet
from pets.serializers import PetSerializer
import ipdb


class PetView(APIView):
    def get(self, request: Request) -> Response:
        # QuerySet
        pets = Pet.objects.all()
        serializer = PetSerializer(instance=pets, many=True)

        return Response(data=serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:

        # Validating input data:
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error, status.HTTP_400_BAD_REQUEST)

        pet = Pet.objects.create(**serializer.validated_data)

        # Formatting output object:
        serializer = PetSerializer(pet)

        return Response({serializer.data, status.HTTP_201_CREATED})
