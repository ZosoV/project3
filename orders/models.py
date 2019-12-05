#author: Oscar Guarnizo
#university: Yachay Tech
#course: Web Programming 2019


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# General class to store the menu items
class MenuItem(models.Model):
    name = models.CharField(max_length = 30)
    size = models.CharField(max_length = 10)
    type = models.CharField(max_length = 30)
    prize = models.FloatField()
    num_toppings = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.type}, {self.name}, {self.size}, {self.prize}"

# extra sauces and stuff
class Extra(models.Model):
    name = models.CharField(max_length = 30)
    prize = models.FloatField()
    menuitems = models.ManyToManyField(MenuItem)
    def __str__(self):
        return f"{self.id} - {self.name} + {self.prize}"


# topping options 
class Topping(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return f"{self.id} - {self.name}"

################################### helper tables to store user preferences ################
# In the data base normal and super users are stored in auth_user

#admin
class Order(models.Model):
    status = models.CharField(max_length = 30, default = 'Open') # the default option is always set because there is not another state unless the user changes it.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many orders are make for an user

    def __str__(self):
        display = f"ID: {self.id} - Status:{self.status} - Username: {self.user} - Total: {self.total} "

        return display

    @property
    def total(self):
        total = 0
        for orderitem in self.orderitem_set.all():
            total += orderitem.cost
        return total

#admin
#store individual orders
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    extras = models.ManyToManyField(Extra)
    quantity = models.IntegerField(default = 1)

    def __str__(self):
        display = f"{self.quantity} x {self.menuitem.type}, {self.menuitem.name}, {self.menuitem.size}"

        if self.toppings.count() > 0:
            display += " - Toppings: "
        for topping in self.toppings.all():
            display +=f" {topping.name},"
        if self.extras.count() > 0:
            display += " -  Extras: "
        for extra in self.extras.all():
            display +=f" {extra.name},"

        display += f" - Prize: {self.cost}"
        return display

    @property
    def cost(self):
        cost = self.menuitem.prize
        for extra in self.extras.all():
            cost += extra.prize
        cost = cost*self.quantity
        return cost
