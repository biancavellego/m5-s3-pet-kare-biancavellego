from rest_framework.views import APIView, Request, Response, status
from groups.models import Group
from groups.serializers import GroupSerializer
import ipdb


class GroupView(APIView):
    ...
