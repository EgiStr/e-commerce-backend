from django.db import models

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from django.contrib.auth.base_user import BaseUserManager

from django.core.validators import RegexValidator

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999 / 08++'. Up to 15 digits allowed.")
  
    # requeired

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_(' Username '),max_length=50)

    # opsional 
    profile = models.ImageField(upload_to='profile', height_field='height_field', width_field='width_field',blank=True, null=True) 
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True) # validators should be a list


    # super user section
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # store area / mau dagang harus ada ini

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_location(self):
        qs = self.user_address.all()
        return qs
        
    def get_order_history(self):
        qs = self.order.all()
        return qs

class Store(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999 / 08++'. Up to 15 digits allowed.")
  
    pemilik = models.OneToOneField(CustomUser,related_name="store",on_delete=models.CASCADE) 
    name = models.CharField(_("name your store"), max_length=70 , unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    about = models.TextField(_(" desc about your store ") , max_length=600, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return  self.name
    
    def get_location(self):
        return self.store_address.all()
    
    def get_product(self):
        return self.product.all()

class Location(models.Model):
    CHOICE = (
        ('costomer','costumer'),
        ('store','store'),
    )

    geolocation = models.CharField(max_length=50) # use third party
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    
    # pemilik location
    user = models.ForeignKey('CustomUser', related_name='user_address', on_delete=models.CASCADE,blank=True, null=True)
    store = models.ForeignKey("Store", related_name="store_address", on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=50,choices=CHOICE)

    def __str__(self) -> str:
        try:
            name = self.user.username + " address Privacy euy!"
        except Exception as e:
            name = self.store.name + " address Privacy euy!"
        return name

class TokenNotif(models.Model):
    user = models.ForeignKey("CustomUser", related_name="tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username + " token"