from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    #blank = true means that you do not have to put anything in the fields
    memo = models.TextField(blank=True)
    #auto_new_add autogenerates a time stamp on there at that moment with DateTimeField
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # we will be using a forign key to connect one model to the other that
    #stores relationship - this will take id of user and save it into this fields
    # gets haleys todo objects where user is equal to the id/ForeignKey
    # a todo can only belong to one key but many todos can stick with many keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # this allows the view within the admin page to read title and not jus todo object

    def __str__(self):
        return '{} , {}'.format(self.title, self.created)
