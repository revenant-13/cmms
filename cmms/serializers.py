from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Equipment, Part, Task, Schedule
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_info', 'address', 'is_active']

class EquipmentSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'model', 'serial', 'parent', 'location_status',
            'expected_return_date', 'vendor', 'is_active', 'children'
        ]

    def get_children(self, obj):
        # Recursively serialize child equipment
        children = obj.get_children()
        return EquipmentSerializer(children, many=True).data

class PartSerializer(serializers.ModelSerializer):
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all())
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Part
        fields = [
            'id', 'part_number', 'status', 'last_updated',
            'equipment', 'vendor', 'is_active'
        ]

class TaskSerializer(serializers.ModelSerializer):
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'description', 'frequency', 'equipment',
            'start_date', 'task_type', 'priority', 'assigned_to'
        ]

class ScheduleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'task', 'due_date', 'completion_date',
            'status', 'history_log', 'is_overdue'
        ]