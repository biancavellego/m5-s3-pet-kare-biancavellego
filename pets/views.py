from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet


# Create your views here.
class PetView(APIView):
    def get(self, request: Request) -> Response:
        # QuerySet
        pets = Pet.objects.all()

        return Response({"message": "Get Route"})

    def post(self, request: Request) -> Response:
        return Response({"message": "Post Route"})
