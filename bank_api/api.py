from rest_framework import generics, status, mixins
from rest_framework.response import Response
from django.http import Http404
from bank.models import Account, Ledger
from .serializers import AccountSerializer, TransferSerializer
from .permissions import IsOwnerOrNoAccess


class AccountExists(generics.ListAPIView):
    serializer_class = AccountSerializer

    # def get_queryset(self):
    #     queryset = Account.objects.get(pk=self.kwargs['pk'])
    #     return queryset

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Transfer(generics.ListCreateAPIView, mixins.CreateModelMixin):
    serializer_class = TransferSerializer

    # def create(self, serializer):
    #     # queryset = SignupRequest.objects.filter(user=self.request.user)
    #     # if queryset.exists():
    #     #     raise ValidationError('You have already signed up')
    #     # serializer.save(user=self.request.user)
    #     debit_account = serializer.data['debit_account']
    #     debit_text = serializer.data['debit_text']
    #     credit_account = serializer.data['credit_account']
    #     credit_text = f'External transfer. recipient: {debit_account}'
    #     amount = float(serializer.data['amount'])
    #     Ledger.transfer(debit_account=debit_account,
    #                     credit_account=credit_account,
    #                     credit_text=credit_text,
    #                     debit_text=debit_text,
    #                     amount=amount
    #                     )

    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     # send_email_confirmation(user=self.request.user, modified=instance)
