from datetime import datetime, timedelta, time
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *

# 타이머 조회, 타이머 수정
class TimerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    
    def get_object(self):
        timer = Timer.objects.get(user=self.request.user)
        return timer
        
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
# 타이머 실행(타이머 푸쉬 객체 생성)
@api_view(['POST'])
def start_timer(request):
    timer = Timer.objects.get(user=request.user)
    timer_push = TimerPush.objects.create(title='Sickret Care 타이머 알람', timer=timer)
    timer_push.save()
    return Response({'detail': f'{timer.interval}분 후에 알람이 전송됩니다. '})

# 알람 리스트 조회, 알람 생성
class AlarmListCreateAPIView(generics.ListCreateAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    
    def list(self, request):
        user = request.user
        alarms = Alarm.objects.filter(user=user)
        alarms_serializers = AlarmSerializer(alarms, many=True)
        return Response(data=alarms_serializers.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        alarm = Alarm.objects.get(id=serializer.data.get('id'))
        
        current_time = timezone.now()
        current_hms = time(hour=current_time.hour, minute=current_time.minute, second=current_time.second)
        
        if alarm.time < current_hms:
            push_time = datetime.combine(current_time.date(), alarm.time)
        else:
            push_time = datetime.combine(current_time.date() + timedelta(days=1), alarm.time)
            
        alarm_push = AlarmPush.objects.create(title=alarm.title, time=push_time, alarm=alarm)
        alarm_push.save()
        
# 알람 단일 조회, 수정(PUT), 삭제
class AlarmRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'alarm_id'