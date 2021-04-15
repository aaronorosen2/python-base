from rest_framework import serializers

from .models import Event , User


class EventSerializer(serializers.ModelSerializer):

    attending_users = serializers.SerializerMethodField(read_only = True )
    total_users = serializers.SerializerMethodField(read_only = True )
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'date',
            'start_time',
            'end_time',
            'created_date',
            'attending_users',
            'total_users'
        ]

    def get_attending_users(self, obj):
        users = obj.user_set.all()
        return UserSerializer(users , many=True ).data

    def get_total_users(self, obj):
        users = obj.get_num_of_users()
        return users



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'