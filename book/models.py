from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']



class Book(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    information = models.CharField(max_length=200)
    total_stock = models.PositiveIntegerField(default=0)
    avail_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '('+str(self.Category)+') ' + str(self.name)


class IssuedBook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    issued_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return str(self.user.name)+'-'+str(self.book.name)