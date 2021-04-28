from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User, Project, Ticket, TicketComment


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), many=True, required=False)

    tickets = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), many=True, required=False)

    comments = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'date_joined', 'github_username', 'projects', 'tickets', 'comments']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# Serializes new user sign ups that responds with the new user's information including a new token.
class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['token', 'username', 'password', 'first_name',
                  'last_name', 'email', 'github_username']


class ProjectSerializer(serializers.ModelSerializer):
    developer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    tickets = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'developer', 'tickets']


class TicketSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=False)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), many=False)

    comments = serializers.PrimaryKeyRelatedField(
        queryset=TicketComment.objects.all(), many=True, required=False)

    class Meta:
        model = Ticket
        fields = ['id', 'priority', 'type', 'description',
                  'status', 'created_at', 'author', 'project', 'comments']


class TicketCommentSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), many=False)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=False)

    class Meta:
        model = TicketComment
        fields = ['id', 'comment', 'created_at',
                  'author', 'ticket']
