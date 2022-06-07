from django.db import transaction
from rest_framework import serializers
from .models import Entity, ExternalLedger
from bank.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id']
        model = Account


class TransferStatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['reference', 'status']
        read_only = ['reference']
        model = ExternalLedger

    # external entity can only validate
    status = serializers.ChoiceField(
        choices=ExternalLedger.ExternalTransactionStatus.VALIDATED)

    def update(self, instance, validated_data):
        # at this point we know the ledger instance belongs to the entity
        # we highjack the update to update our ledger, and then call the super
        our_ledger = ExternalLedger.objects.filter(
            reference=instance.reference).last()
        our_ledger.status = validated_data['status']
        our_ledger.save()

        return super().update(instance, validated_data)


class TransferSerializer(serializers.Serializer):

    amount = serializers.FloatField(write_only=True)
    reference = serializers.IntegerField(write_only=True)
    recipient_account = serializers.IntegerField(write_only=True)
    recipient_text = serializers.CharField(max_length=100, write_only=True)
    transaction = serializers.IntegerField(read_only=True)

    def get_entity(self):
        return Entity.objects.get(user=self.context['request'].user)

    def validate_reference(self, value):
        if ExternalLedger.reference_exists(reference=value, entity=self.get_entity()):
            raise serializers.ValidationError(
                "Reference for this entity already exists, try getting status of transfer")
        else:
            return value

    def validate_recipient_account(self, value):
        try:
            return Account.objects.get(pk=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                "Recipient account doesn't exist")

    def create(self, validated_data):
        validated_data['entity'] = self.get_entity()
        return ExternalLedger.transfer(**validated_data)

    def update(self, validated_data):
        return ExternalLedger.transfer(**validated_data)
