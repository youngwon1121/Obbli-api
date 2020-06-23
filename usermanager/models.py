from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class MyUserManager(BaseUserManager):
    def create_user(self, userid, username, phone, date_of_birth, email, password=None):
        if not userid:
            raise ValueError('User must have an userid')

        user = self.model(
            userid = userid,
            username = username,
            phone = phone,
            date_of_birth = date_of_birth,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, username, phone, date_of_birth, email, password=None):
        user = self.create_user(userid=userid, 
            username=username,
            phone=phone, 
            date_of_birth=date_of_birth, 
            email=email, 
            password=password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    userid = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    graduated_school = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['username', 'phone', 'date_of_birth', 'email']

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def __str__(self):
        return self.userid
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class ResetPW(models.Model):
    email = models.EmailField(max_length=255)
    hash_key = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}".format(self.email, self.created_at)