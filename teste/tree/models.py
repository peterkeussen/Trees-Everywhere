from datetime import datetime
from typing import List, Tuple
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


# Account
class Account(models.Model):
    name = models.CharField(_('Name'), max_length=60)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    active = models.BooleanField(default=True)
    # Many account for user
    user = models.ManyToManyField(User, verbose_name=_(
        "Users"), related_name='users_accounts', blank=True)
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        
    def __str__(self) -> str:
        return self.name

    
class Tree(models.Model):
    name = models.CharField(_('Name'), max_length=60)
    scientific_name = models.CharField(_('Scientific Name'), max_length=60)

    class Meta:
        verbose_name = _('Tree')
        verbose_name_plural = _('Trees')
        
    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField(_('Planted at'))
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, verbose_name=_(
        "Tree"), on_delete=models.CASCADE)
    account = models.ForeignKey(Account, verbose_name=_("Account"), on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        verbose_name = _('Tree Planted')
        verbose_name_plural = _('Trees Planted')
        ordering = ('planted_at',)
        
    def __str__(self) -> str:
        return self.planted_at.__str__()

    def location(self, lat: float, log: float):
        return (lat,log)  

    def get_absolute_url(self):
        return reverse('tree_detail', args=[str(self.id)])


# Extending user model using a proxy model
class User(User):
    class Meta:
        proxy = True
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def plant_tree(self, tree: Tree, location: Tuple):
        user = User.objects.get(pk=self.pk)
        account = Account.objects.get(user=user)
        PlantedTree.objects.create(age=0, 
                           user=user, 
                           planted_at=datetime.now(), 
                           account=account,
                           tree=tree,
                           latitude=location[0],
                           longitude=location[1])
    
    def plant_trees(self, plants: List):
        user = User.objects.get(pk=self.pk)
        account = Account.objects.get(user=user)
        
        for plant in plants:
            PlantedTree.objects.create(age=0, 
                           user=user, 
                           planted_at=datetime.now(), 
                           account=account,
                           tree=Tree.objects.filter(name=plant[0][0]),
                           latitude=plant[0][1][0],
                           longitude=plant[0][1][1]
                        )


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='profile_user')
    about = models.TextField(_('About'), blank=True)
    joined = models.DateTimeField()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self) -> str:
        return self.user.__str__()
    
    def get_absolute_url(self):
        return reverse('home')

