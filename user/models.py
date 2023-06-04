from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """用户表"""
    username = models.CharField(verbose_name='用户名', max_length=255)
    password = models.CharField(verbose_name='密码', max_length=150)
    email = models.CharField(verbose_name='邮箱', max_length=255)
    create_time = models.DateField(verbose_name='注册时间')
    role = models.ForeignKey(verbose_name='用户角色', to='Role', to_field='id', on_delete=models.CASCADE)
    depart = models.ForeignKey(verbose_name='用户部门', to='Department', to_field='id', null=True, blank=True,
                               on_delete=models.SET_NULL)
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=150)

    def __str__(self):
        return self.title


class Role(models.Model):
    """角色表"""
    caption = models.CharField(verbose_name='角色名称', max_length=150)
    caption_type = models.IntegerField(verbose_name='角色类型')

    def __str__(self):
        return self.caption
