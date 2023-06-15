from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """用户表"""
    username = models.CharField(verbose_name='用户名', max_length=255)
    fullname = models.CharField(verbose_name='姓名', max_length=255)
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


class SalesInfo(models.Model):
    # 文件分类数据
    sort_choices = (
        (1, '公司白皮书'),
        (2, '公司销售白皮书'),
        (3, 'O32系统'),
        (4, 'TA系统'),
        (5, '东方证券'),
        (6, '光大证券'),
        (7, '国金证券'),
        (8, '国元证券'),
        (9, '海通证券'),
        (10, '券商周末测试'),
        (11, '自动化平台'),
        (12, '测试管理平台'),
        (13, '环境配置管理'),
        (14, '客户行为回放'),
        (15, '手机自动化平台'),
        (16, '数据构造平台'),
        (17, '统一模拟'),
        (18, '小工具介绍'),
        (19, 'MicroFocus(OpenText)'),
        (20, '社保'),
        (21, '长鑫存储'),
    )

    filename = models.CharField(verbose_name='文件名', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    sort = models.IntegerField(verbose_name='所属分类', choices=sort_choices)
    # sort_id = models.IntegerField(verbose_name='分类id')
    filepath = models.FileField(verbose_name='文件路径', max_length=128, upload_to='sales/%Y-%m-%d')
    user = models.ForeignKey(verbose_name='负责人', to='UserInfo', to_field='id', null=True, blank=True,
                             on_delete=models.SET_NULL)
    update_time = models.DateTimeField(verbose_name='更新时间')
    renew = models.CharField(verbose_name='更新说明', max_length=255)


class ExcelInfo(models.Model):
    type_choices = (
        (1, '光大_综合账户'),
        (2, '东方_融资融券'),
    )
    file_type = models.IntegerField(verbose_name='所属分类', choices=type_choices, null=True, blank=True)
    file_title = models.CharField(verbose_name='文件名称', max_length=255, null=True, blank=True)
    issue_description = models.TextField(verbose_name='问题描述', max_length=255, null=True, blank=True)
    issue_type = models.CharField(verbose_name='问题分类', max_length=255, null=True, blank=True)
    issue_module = models.CharField(verbose_name='所属模块', max_length=255, null=True, blank=True)
    issue_problem = models.TextField(verbose_name='问题原因', max_length=255, null=True, blank=True)
    issue_analysis = models.TextField(verbose_name='影响面分析', max_length=255, null=True, blank=True)
    test_strategy = models.TextField(verbose_name='测试策略', max_length=255, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
