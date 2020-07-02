from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=53)

    class Meta:
        verbose_name = '组信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    user_type_choice = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_choice)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=0)
    def get_username(self):
        return self.username + '123'

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=129)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class Role(models.Model):
    title = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    number = models.IntegerField()

    class Meta:
        # db_table
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        # verbose_name_plural
        # ordering = ['']

    def __str__(self):
        return self.title


class Data(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=123)

    class Meta:
        verbose_name = '数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=75)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 小数位

    class Meta:
        db_table = 'book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AuthorDetail(models.Model):
    mobile = models.CharField(max_length=11)
    home = models.CharField(max_length=20)
    author = models.OneToOneField(to='Author',
                                related_name = 'detail',
                                on_delete=models.CASCADE,
                                db_constraint = False,
                                )
    class Meta:
        db_table = 'author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.name+'_详情'

class NewBook(models.Model):
    name = models.CharField(max_length=20)
    author  =models.ManyToManyField(to='Author',
                                    db_constraint = False,
                                    related_name = 'book'
                                    )
    publish = models.ForeignKey(to='Publish',
                                on_delete=models.CASCADE,
                                db_constraint = False,
                                related_name = 'publish'
                                )
    is_delete = models.BooleanField(default=0)
    @property
    def get_author(self):
        ret = []
        for i in self.author.all():
            ret.append(i.name)
        return ret
    @property
    def get_publish(self):
        return self.publish.name

    class Meta:
        db_table = 'books'
        verbose_name = '新青年书籍'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

