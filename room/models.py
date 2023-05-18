from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.text import slugify


class RoomType(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_images')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
  

class RoomQuerySet(models.QuerySet):
    def search_room(self, check_in, check_out, room_type):
        return self.filter(
            Q(roomtype__id=room_type) & 
            Q(date__lt=check_out) &
            Q(date__gte=check_in)
        ).distinct()
    
    def filter_available_room(self, check_in, check_out, room_type):
        return self.search_room(check_in, check_out, room_type).filter(is_available=True)

    def filter_unavailable_room(self, check_in, check_out, room_type):
        return self.search_room(check_in, check_out, room_type).filter(is_available=False)


class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)
    
    def search_available(self, check_in, check_out, room_type):
        return self.get_queryset().filter_available_room(check_in, check_out, room_type)

    def filter_unavailable(self, check_in, check_out, room_type):
        return self.get_queryset().filter_unavailable_room(check_in, check_out, room_type)


class Room(models.Model):
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    
    objects = RoomManager()


class Stock(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    number_of_rooms = models.PositiveIntegerField()


@receiver(pre_save, sender=Room)
def update_room_availability(sender, instance, **kwargs):
    print('update_room_availability')
    if instance.stock.number_of_rooms == 0:
        instance.is_available = False