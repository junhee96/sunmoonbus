from django.contrib import admin
from .models import *

admin.site.register(Bus)
admin.site.register(StartTime)
admin.site.register(Seat)
admin.site.register(Reservation)