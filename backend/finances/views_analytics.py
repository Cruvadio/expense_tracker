import json
import datetime

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_celery_beat.models import PeriodicTask, CrontabSchedule, \
    IntervalSchedule
from rest_framework.viewsets import ViewSet

from .serializers import ScheduleSerializer
from .utils import get_analytics
from .models import Transaction


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        params = request.query_params
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        qs = Transaction.objects.filter(owner=user)
        if start_date and end_date:
            qs = Transaction.objects.filter(date__gte=start_date,
                                            date__lte=end_date)

        analytics = get_analytics(qs)

        return Response(analytics)


class WeeklyReportViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        user = request.user
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            time: datetime.time = serializer.validated_data['time']
            day_of_week = serializer.validated_data['day_of_week']
            #schedule, _ = CrontabSchedule.objects.get_or_create(
            #    hour=str(time.hour), minute=str(time.minute),
            #    day_of_week=day_of_week
            #)
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.SECONDS
            )
            task, _ = PeriodicTask.objects.get_or_create(
                #crontab=schedule,
                interval=schedule,
                name=f'{request.user.username} - weekly news subscription',
                task='finances.tasks.send_weekly_report',
                args=json.dumps([user.id, user.email])
            )
            return Response({
                'task_id': task.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='unsubscribe')
    def unsubscribe(self, request, pk=None):
        task = get_object_or_404(PeriodicTask, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
