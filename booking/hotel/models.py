from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator,MaxValueValidator


class UserProfile(AbstractUser):

    user = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0, null=True, blank=True,
                                      validators=[MinValueValidator(0),MaxValueValidator(100)])
    phone_number = PhoneNumberField(null=True,blank=True,region='KG')
    ROLE_CHOICES = (
        ('клиент', 'клиент'),
        ('владелец', 'владелец'),
        ('Администратор', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def str(self):
        return self.user


class Hotel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,verbose_name='владелец')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField(default=True)  # активен/неактивен
    photos = models.ImageField(upload_to='hotel_photos/', blank=True, null=True)

    def str(self):
        return f'{self.name} - {self.status} - {self.photos}'


    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class HotelPhotos(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    hotel_image = models.ImageField(upload_to='hotel_images/')


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена', default=0)
    number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('доступно', 'доступно'),
                                                      ('забронировано', 'забронировано'),
                                                      ('оккупировано', 'оккупировано')])
    photos = models.ImageField(upload_to='room_photos/', blank=True, null=True)

    def str(self):
        return f'{self.number} - {self.status} - {self.photos}'


class RoomPhotos(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='room_images/')


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('room', 'start_date', 'end_date')  # Уникальность бронирования по дате

    def save(self, *args, **kwargs):
        if not self.pk:  # Если это новое бронирование
            if self.room.status != 'доступно':
                raise ValueError("Номер не доступен для бронирования.")
            self.room.status = 'забронировано'  # Обновляем статус номера
            self.room.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.room.status = 'доступно'  # Обновляем статус номера на доступный
        self.room.save()
        super().delete(*args, **kwargs)


class BookingManager(models.Manager):
    def is_room_available(self, room, start_date, end_date):
        return not self.filter(
            room=room,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()


class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.hotel} - {self.user}'



