# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class User(models.Model):
    def __unicode__(self):
        return u'%s' % (self.login)
    
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    name = models.CharField(max_length=80, verbose_name='nome')
    email = models.EmailField(unique=True, verbose_name='e-mail')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='sexo')
    login = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=10, verbose_name='senha')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='foto')

class Post(models.Model):
    def __unicode__(self):
        return u'%s - %s' % (self.user, self.message)
    
    
    user = models.ForeignKey('User', verbose_name='usuário')
    message = models.CharField(max_length=140, verbose_name='mensagem')
    date = models.DateTimeField(verbose_name='data')

class Follow(models.Model):
    def __unicode__(self):
        return u'%s -> %s' % (self.user, self.follows)
    
    user = models.ForeignKey('User', verbose_name='usuário')
    follows = models.ForeignKey('User', related_name='segue')
#    date = models.DateTimeField(verbose_name='data')
