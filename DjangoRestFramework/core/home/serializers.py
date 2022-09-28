from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color_name']

class PersonSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = "__all__"

    def get_country(self, obj):
        return "India"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("username is taken")

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'] )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
