import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer  # type: ignore
from asgiref.sync import async_to_sync
from .models import Subscription
from auths.models import CustomUser


@receiver(post_save, sender=Subscription)
def send_subscription_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user_channel = instance.user.username  

        async_to_sync(channel_layer.group_send)(
            user_channel,
            {
                "type": "subscription_created",
                "message": "Subscription successfully created",
                "amount": str(instance.amount),  
                "tier": instance.tier,
                "status": instance.status,
            },
        )


@receiver(post_save, sender=CustomUser)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user=instance,
            amount=0.0,
            transaction_id=None,
            tier='basic',
            status='unpaid'
        )