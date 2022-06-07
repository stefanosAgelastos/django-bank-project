from rest_framework import generics
# this class handles the authorization of the token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
# this custom class issues the token for a valid entity's username and password
from .authentication import EntityAuthentication
from bank.models import Account
from .models import ExternalLedger
from .serializers import AccountSerializer, TransferSerializer, TransferStatusSerializer
from .permissions import IsOwnerOrNoAccess

local_authentication_classes = [EntityAuthentication, TokenAuthentication]


class AccountExists(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class Transfer(generics.CreateAPIView):
    authentication_classes = local_authentication_classes
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer


class TransferStatus(generics.RetrieveUpdateAPIView):
    authentication_classes = local_authentication_classes
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess]
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
