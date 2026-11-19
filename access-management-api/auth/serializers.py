from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserMeSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

    def get_groups(self, user):
        return list(user.groups.values_list('name', flat=True))


class GroupTypePathParamSerializer(serializers.Serializer):
    type = serializers.CharField()

    def validate_type(self, value):
        if not Group.objects.filter(name=value).exists():
            raise serializers.ValidationError(f'Unknown Pokemon type: {value}')
        return value
