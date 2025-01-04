from rest_framework import serializers
from accounts.models import UserModel
from rest_framework.authtoken.models import Token 
from rest_framework.validators import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length =100, required=True) 
    username = serializers.CharField(max_length = 45,)
    password = serializers.CharField(min_length = 8, write_only = True, required=True)  
    
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password']
        # fields = ['id','email', 'username', 'password'] if I want the auto generated id on the database to be added

    
    def validate(self, attrs):
        email_exists = UserModel.objects.filter(email = attrs['email']).exists()
        if email_exists: 
            raise ValidationError('Email has already been used')
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user