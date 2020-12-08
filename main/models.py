# 2015244044 이준희
# 지역,시간,좌석,예약 데이터베이스
from django.db import models
from accounts.models import User
from django.conf import settings


class Bus(models.Model):
    busid = models.PositiveIntegerField(primary_key=True)
    busname = models.CharField(max_length=50)

    def __str__(self):
        return self.busname


class StartTime(models.Model):
    startid = models.CharField(max_length=20, primary_key=True)
    busid = models.ForeignKey(Bus, on_delete=models.CASCADE)
    startdate = models.DateField()
    starttime = models.TimeField()

    def __str__(self):
        return "{0}/{1}".format(self.startdate, self.starttime)
    class Meta:
        ordering = ['-startid'] 

class Seat(models.Model):
    seatid = models.IntegerField(primary_key=True)
    startid = models.ForeignKey(StartTime, on_delete=models.CASCADE)
    seatrow = models.IntegerField()
    seatcol = models.CharField(max_length=11)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{0}{1}".format(self.seatcol, self.seatrow)


class Reservation(models.Model):
    reservationid = models.CharField(max_length=20, primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    startid = models.ForeignKey(StartTime, on_delete=models.CASCADE)
    busid = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seatid = models.ForeignKey(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return self.reservationid