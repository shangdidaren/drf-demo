from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from app import models


class Update_ListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance

class Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Data
        fields = '__all__'

        # todo 关联自定义的ListSerializer类
        # list_serializer_class = serializers.Update_ListSerializer
        # 默认是群操作会使用ListSerializer，但是没有实现update的群方法

class Userinfo_Serializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.title')

    class Meta:
        model = models.UserInfo
        fields = ['get_user_type_display', 'username', 'group']


class NewBook_Serializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if '黄' in value:
            raise ValidationError('改H书不能出版')
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get('publish')
        name = attrs.get('name')
        if models.NewBook.objects.filter(name=name, publish=publish, is_delete=0):
            raise ValidationError({'book': '该出版社已经存在这本书'})
        return attrs

    class Meta:
        model = models.NewBook
        fields = ['name', 'author','get_publish', 'publish','get_author']

        extra_kwargs = {
            # write_only
            # 可以安排authors进行显示，使用author来存储，
            # 传值的类型可以通过让Read—only=true打开看一下
            'author': {
                'required': True,
                'write_only': True,
            },
            'publish': {
                'required': True,
                'write_only': True,
            },
            # double
            'name': {
                'required': True,
            },

            # read_only
            'get_publish':{
                'read_only':True,
            },
            'get_author':{
                'read_only':True,
            },

        }
