import shelve
from utils import Product

"""
with shelve.open('Products','c') as Products:
    Products['Анимашки'] = {}
#    Products['Смайлики'] = {'test': Product(20,1),'test2':Product(20,1)}

with shelve.open('Admins','c') as Admins:
    Admins['categs_price'] = {}
"""
with shelve.open('Users','c') as Users:
    user = Users['1274864704']
    user.balance += 50000 
    user.role.name = 'admin'
    user.role.get_admin = True
    Users['1274864704'] = user
