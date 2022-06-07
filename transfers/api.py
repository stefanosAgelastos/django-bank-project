from rest_framework import generics, status, mixins
from rest_framework.response import Response
from django.http import Http404
from bank.models import Account
from .models import ExternalLedger
from .serializers import AccountSerializer, TransferSerializer, TransferStatusSerializer
from .permissions import IsOwnerOrNoAccess


class AccountExists(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class Transfer(generics.CreateAPIView):
    serializer_class = TransferSerializer


class TransferStatus(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrNoAccess]
    serializer_class = TransferStatusSerializer
    http_method_names = ["patch", "get", "options", "head"]

    def get_queryset(self):
        return ExternalLedger.objects.filter(reference=self.kwargs['reference'])

    def get_object(self):
        try:
            # only the first ledger belongs to the creditor entity
            obj = self.get_queryset().first()
        except ExternalLedger.DoesNotExist:
            raise Http404("Transaction does not exist.")
        self.check_object_permissions(self.request, obj)
        return obj
