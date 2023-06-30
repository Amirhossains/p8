import random

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import User, Device

class RegesterView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Respones(status=status.HTTP_400_BAD_REQUEST)

        