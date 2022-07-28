from rest_framework import serializers
from apps.users.models.seller import Seller


class SellerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ('id', 'company_registration_number', 'company_name', 'company_owner_name',
                  'company_location', 'bank_name', 'account_holder_name', 'account_number')

    def create(self, validated_data):
        request = self.context.get("request")
        if (request.user.id == None):
            raise serializers.ValidationError("헬로")
        seller = Seller.objects.create(
            company_registration_number=validated_data['company_registration_number'],
            company_name=validated_data['company_name'],
            company_owner_name=validated_data['company_owner_name'],
            company_location=validated_data['company_location'],
            bank_name=validated_data['bank_name'],
            account_holder_name=validated_data['account_holder_name'],
            account_number=validated_data['account_number'],
            user_id=request.user.id,
        )
        return seller
