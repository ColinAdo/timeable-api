from django.dispatch import receiver
from django.db.models.signals import post_save

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore

from .models import Subscription
from auths.models import CustomUser

# Add post save signal to Subscription model
@receiver(post_save, sender=Subscription)
def send_subscription_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    user_channel = instance.user.username  

    async_to_sync(channel_layer.group_send)(
        user_channel,
        {
            "type": "subscription_updated",
            "message": "Subscription successfully updated" if not created else "Subscription successfully created",
            "amount": str(instance.amount),  
            "tier": instance.tier,
            "status": instance.status,
        },
    )

# Add post save signal to wedsocket
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