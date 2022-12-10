from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from Web import settings
from chatapp.serializers import MsgSerializer
from chatapp.models import Msg

class CsrfExempt(SessionAuthentication): # Disable csrf *(try to set later)
    def enforce_csrf(self, request):
        return

class MsgPagination(PageNumberPagination):
    page_size = 18       # Number of Messages to load

class MsgViewSet(ModelViewSet):
    queryset = Msg.objects.all()
    serializer_class = MsgSerializer
    allowed_methods = ('GET','POST','HEAD','OPTIONS')
    authentication_classes = (CsrfExempt,)
    pagination_class = MsgPagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(sender = request.user) | Q(receiver = request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset =  self.queryset.filter(Q(sender = request.user, receiver__username = target) |
                                                  Q(sender__username = target, receiver = request.user) )
        return super(MsgViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(self.queryset.filter(Q(sender = request.user) | Q(receiver = request.user), Q(pk=kwargs['pk'])))
#        print("Message =", msg)
        serializer = self.get_serializer(msg)
#        print("Serializer =", serializer.data)
        return Response(serializer.data)