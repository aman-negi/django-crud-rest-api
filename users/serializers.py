from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','address','email','password']
        # extra_kwargs ={
        #     "password" : {"write_only" : True}
        # }
        
        
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    
# class UpdateDetail(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'    