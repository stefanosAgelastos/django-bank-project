from django.contrib.auth.models import User
from rest_framework import serializers
from bank.models import Account, Ledger, User as ExternalBankUser


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id']
        model = Account


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['uid', 'customer_account', 'external_bank_account',
                  'amount', 'recipient_text', 'external_bank']
        read_only_fields = ['customer_account', 'external_bank_account',
                            'amount', 'recipient_text', 'external_bank']
        model = Ledger

    customer_account = serializers.IntegerField()
    external_bank_account = serializers.IntegerField()
    amount = serializers.FloatField()
    recipient_text = serializers.CharField(max_length=100)
    external_bank = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_customer_account(self, value):
        try:
            return Account.objects.get(pk=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Debit account doesn't exist")

    def validate_external_bank_account(self, value):
        try:
            return Account.objects.get(pk=value, user=self.context['request'].user)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                "Credit account is not owned by you")

    def create(self, validated_data):
        return Ledger.external_transfer(**validated_data)
