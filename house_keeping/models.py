from django.db import models
from staff.models import staffTable
from rooms.models import roomsTable
# Create your models here.
class houseKeepingTable(models.Model):
    chores = models.CharField(max_length=60, blank=True)
    room = models.ForeignKey(roomsTable, related_name='housekeeping_schedule', on_delete=models.CASCADE)
    staff = models.ForeignKey(staffTable, related_name='schedules', on_delete=models.CASCADE)
    start_date = models.CharField(max_length=60, blank=True)
    end_date = models.CharField(max_length=120, blank=True)
    time = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=120, blank=True)
    created_date= models.DateTimeField(auto_now_add=True)
