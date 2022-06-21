from .models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","password","name","phone")
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        User.objects.filter(
            email = user
        ).update(
            name = validated_data['name'],
            phone = validated_data['phone']
        )
        return user

