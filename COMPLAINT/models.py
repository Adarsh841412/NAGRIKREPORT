# from django.db import models
# from  ACCOUNT.models import UserModel
# from ACCOUNT.models import Officer
# # Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=20, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
# class Complaint(models.Model):
#     STATUS_CHOICE = [('pending','Pending'),('resolve','Resolve'),('inProcess','InProcess'),('invalid','Invalid')]
#     username = models.CharField(max_length=20) 
#     user = models.ForeignKey(UserModel,related_name='user',on_delete=models.CASCADE)
#     assinged_officer = models.ForeignKey(Officer,on_delete=models.CASCADE)
#     category = models.ForeignKey(Category,on_delete=models.SET_NULL)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     location_address= models.CharField(max_length=100)
#     latitude =  models.FloatField() 
#     longitude = models.FloatField() 
#     status = models.CharField(max_length=50,choices=STATUS_CHOICE)
#     priority = models.IntegerField() 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    





