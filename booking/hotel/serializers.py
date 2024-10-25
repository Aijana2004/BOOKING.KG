from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'phone_number', 'first_name', 'last_name', 'age']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,


            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),



        }


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

        def get_average_rating(self, obj):
            return obj.get_average_rating()


class HotelPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelPhotos
        fields = '__all__'


class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoomPhotos
        fields = '__all__'

class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'start_date', 'end_date']

    def validate(self, attrs):
        room = attrs.get('room')
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if not Booking.objects.is_room_available(room, start_date, end_date):
            raise serializers.ValidationError("Номер уже забронирован на эти даты.")

        return attrs

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'