from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class CustomUser(AbstractBaseUser):
    """
    This class replaces django basic user with custom user model.
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField('staff status', default=False)

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    def __str__(self):
        return str(self.email)

    @staticmethod
    def get_by_id(user_id):
        """Returns user by id"""
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            print("User does not exist")

    @staticmethod
    def create(first_name, last_name, phone, email, password):
        """Creates CustomUser instance"""
        user = CustomUser(first_name=first_name,
                          last_name=last_name,
                          phone=phone,
                          email=email)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_by_email(email):
        """Returns user by email"""
        try:
            user = CustomUser.objects.get(email=email)
            return user
        except CustomUser.DoesNotExist:
            print("User does not exist")

    @staticmethod
    def delete_user_by_id(user_id):
        user = CustomUser.get_by_id(user_id)
        user.delete()

    def activate(self):
        """
        Activates user.
        """
        self.is_active = True
        self.save()

    def has_perm(self, perm, obj=None):
        """Replaces method required for using django-admin"""
        return True

    def has_module_perms(self, app_label):
        """Replaces method required for using django-admin"""
        return True

    def get_short_name(self):
        """Replaces method required for using django-admin"""
        return self.email

    def set_admin_rights(self, rights=None):
        """
        Gives or takes admin-rights from a user.
        """
        if rights:
            self.is_staff = True
            self.save()
        else:
            self.is_staff = False
            self.save()