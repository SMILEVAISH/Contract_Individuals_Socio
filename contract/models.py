from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

from userApp.models import CustomUser as user



# Create your models here.


'''
Contract Table
'''
class Contract(models.Model):
    owner_id = models.ForeignKey(user, on_delete=models.CASCADE)
    contract_name = models.CharField(max_length=100)
    prticipants = models.ManyToManyField(user, related_name='participants')
    due_date = models.DateTimeField()
    created_on = models.DateField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
    
    

@receiver(post_save, sender=Contract)
def update_is_expired(sender, instance, **kwargs):
    if instance.due_date < timezone.now() and not instance.is_expired:
        instance.is_expired = True
        instance.save()


'''
Adding and removing users Table
'''
class ContractUserRequest(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    to_user = models.ForeignKey(user, blank=True ,on_delete=models.CASCADE)
    sent_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)
    rejected = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'user_request'
        verbose_name_plural = 'user_requests'
    
    def __str__(self):
        return f'{self.to_user} is being requested by contract id : {self.contract}'
    
    def accept(self):
        # User should accept the contract
        self.contract.prticipants.add(self.to_user)
        # self.viewed = timezone.now()
        self.rejected = False
        self.save()
        self.delete()
        # Deleting reverse requests
        # ContractUserRequest.filter(contract = self.contract, to_user = self.to_user).delete()
        return True

    
    def reject(self):
        # User rejecting the contract 
        self.rejected = timezone.now()
        self.save()
        return True

    def view(self):
        # Mark viewed
        self.viewed = timezone.now()
        self.save()
        return True

    def cancel(self):
        # User canceling the request
        self.delete()
        return True
     
