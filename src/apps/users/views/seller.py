from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework import generics
from apps.users.serializers.seller import SellerRegisterSerializer


class SellerRegisterAPI(generics.GenericAPIView):
    serializer_class = SellerRegisterSerializer

    def post(self, request):
        # try:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        seller = serializer.save()
        return JsonResponse({
            "status": True,
            "message": "판매자 가입에 성공했어요",
            "result": {
                'seller': SellerRegisterSerializer(seller, context=self.get_serializer_context()).data,
            }
        }, status=200)
        # except:
        return JsonResponse({'hello': '판매자 가입에 실패했어요'}, status=404)
