from django.contrib import admin

from .models import (
    RoomType,
    Room,
    Stock
)

class StockInline(admin.StackedInline):
    model = Stock
    extra = 0

class RoomAdmin(admin.ModelAdmin):
    inlines = [StockInline, ]
    list_display = ['roomtype', 'date', 'is_available', 'price_per_night']


admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(Stock)