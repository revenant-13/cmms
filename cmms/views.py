from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions
from .models import Vendor, Equipment, Part, Task, Schedule
from .serializers import (
    VendorSerializer, EquipmentSerializer, PartSerializer,
    TaskSerializer, ScheduleSerializer
)

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.filter(is_active=True)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class PartListCreateView(generics.ListCreateAPIView):
    queryset = Part.objects.filter(is_active=True)
    serializer_class = PartSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class PartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()  # No is_active filter since tasks are tied to equipment
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.DjangoModelPermissions]