# # 2015244044 이준희
from django.shortcuts import render,redirect, get_object_or_404,Http404
from accounts.models import *
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
# 메인 페이지
def index(request):
    return render(request, "index.html")

# 시간표 페이지
def about(request):
    return render(request, "about.html")

# 지역 선택
@login_required
def busSelect(request, user_id):
    buss = Bus.objects.all()
    return render(request, 'busSelect.html',{'buss': buss, 'user_id':user_id})

# 시간 선택
@login_required
def startselect(request, user_id, bus_id):
    starttimes = StartTime.objects.filter(busid=bus_id)
    dates = set()
    for starttime in starttimes:
        if starttime.startdate not in dates:
            dates.add(starttime.startdate)
    return render(request, 'starttimeSelect.html', {'starttimes': starttimes, 'user_id': user_id, 'bus_id': bus_id, 'dates': dates})

# 좌석 선택
@login_required
def seatSelect(request, user_id, bus_id, start_id):
    seats = Seat.objects.filter(startid = start_id)
    return render(request, 'seatSelect.html', {'user_id': user_id, 'seats': seats, 'bus_id': bus_id, 'start_id': start_id})

# 좌석 선택시 예약 번호 생김
@login_required
def confirm(request, user_id, bus_id, start_id, seat_id):
    seat_instance = Seat.objects.get(seatid=seat_id)
    seat_instance.status = True
    seat_instance.save()

    reservation_id = "{}-{}-{}".format(user_id, bus_id, seat_id)

    try:
        reservation_instance = Reservation.objects.create(
            reservationid = reservation_id,
            username = User.objects.get(username=user_id),
            busid = Bus.objects.get(busid=bus_id),
            startid = StartTime.objects.get(startid=start_id),
            seatid = Seat.objects.get(seatid=seat_id),
        )
        reservation_instance.save()
    except:
        return seatSelect(request, user_id, bus_id, start_id)
        
    return render(request, 'confirm.html', {'user_id': user_id})


# 예약 내역 페이지
@login_required
def myhistory(request, user_id):
    reservations = Reservation.objects.filter(username=User.objects.get(username=user_id))
    return render(request, 'myhistory.html', {'reservations': reservations, 'user_id': user_id})

# 예약 취소
@login_required
def cancel(request, user_id, reservation_id):
    try:
        reservation_instance = Reservation.objects.get(reservationid=reservation_id)
        seat_id = reservation_instance.seatid
        seat_instance = Seat.objects.get(seatid=seat_id.seatid)
        seat_instance.status = False
        seat_instance.save()

        reservation_instance.delete()

    except:
        return myhistory(request, user_id)
    
    return myhistory(request, user_id)

# 예약 성공
@login_required
def initial(request):
    seats = Seat.objects.all()
    for seat in seats:
        seat.status = False
        seat.save()
    return HttpResponse("성공")