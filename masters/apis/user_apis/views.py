from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers.user_serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "İstifadəçi uğurla yaradıldı.",
                "user": {
                    "id": user.id,
                    "full_name": f"{user.first_name} {user.last_name}",
                    "mobile_number": user.mobile_number
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

"""


{
  "first_name": "Elvin",
  "last_name": "Quliyev",
  "birth_date": "2000-05-12",
  "mobile_number": "501287667",
  "gender": "MALE",
  "profession_area": "Tikinti",
  "profession_speciality": "Usta",
  "experience_years": 5,
  "cities": [1, 2],
  "education": "1",
  "education_speciality": "İnşaat mühəndisliyi",
  "languages": [1, 3],
  "profile_image": null,
  "facebook": "",
  "instagram": "",
  "tiktok": "",
  "linkedin": "",
  "work_images": [],
  "note": "",
  "password": "Izzet-1409",
  "password2": "Izzet-1409"
}



"""