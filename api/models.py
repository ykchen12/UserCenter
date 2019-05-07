from django.db import models
from api.cryp import encrypt_p


class Department(models.Model):
    num = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    # super_department = models.ForeignKey('self', related_name='super', on_delete=True, null=True, blank=True)
    children = models.ManyToManyField('self', related_name='child', null=True, blank=True, default=None)

    def __str__(self):
        return u"%s-%s" % (self.num, self.name)


class User(models.Model):
    user_id = models.IntegerField(null=True, blank=True)  # 员工工号
    account = models.CharField(max_length=30, null=True, blank=True)  # 员工账号
    name = models.CharField(max_length=30, null=True, blank=True)  # 员工姓名
    password = models.CharField(max_length=255, null=True, blank=True)  # 员工密码
    email = models.EmailField(max_length=255, null=True, blank=True)  # 员工邮箱
    department = models.ForeignKey(Department, related_name='depart_name', on_delete=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = encrypt_p(self.password)
            super(User, self).save(*args, **kwargs)
        else:
            self.password = encrypt_p('123456')
            super(User, self).save(*args, **kwargs)

    def __str__(self):
        return u"%s" % self.name


class UserToken(models.Model):
    user = models.OneToOneField(to=User, on_delete=True)
    token = models.CharField(max_length=64)
