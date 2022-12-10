from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField
from chatapp.models import Msg
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class MsgSerializer(serializers.ModelSerializer):
    sender = CharField(source = "sender.username", read_only = True)
    receiver = CharField(source = "receiver.username")

    def create(self, validated_data):
#        print("started create()")
#        print(validated_data)
        sender = self.context['request'].user
        receiver = get_object_or_404(User, username = validated_data["receiver"]["username"])
        msg = Msg(sender = sender, receiver = receiver, content = validated_data['content'])
        msg.save()
#        print("Msg created")
        return msg

    class Meta:
        model = Msg
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp')