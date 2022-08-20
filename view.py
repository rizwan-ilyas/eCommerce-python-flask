from itertools import product


class Product:
    def __init__(self,name,price,desc,discount,catagory,sellerId,quantity,image=""):
        self.name=name
        self.price=price
        self.description=desc
        self.discount=discount
        self.catagory=catagory
        self.seller_id=sellerId
        self.quantity=quantity
        self.image=image




class User:
    def __init__(self,email,password,type="buyer",profileStatus=False):
        self.email=email
        self.password=password
        self.type=type
        self.profileStatus=profileStatus

class Buyer:
    def __init__(self,name,contact,s_email,c_address,p_address,image="profile.png",balance=0):
        self.image=image
        self.name=name
        self.contact=contact
        self.s_email=s_email
        self.c_address=c_address
        self.p_address=p_address
        self.balance=balance

class Seller:
    def __init__(self,name,contact,address,bussinssType,totalProducts,image="profile.png",balance=0):
        self.image=image
        self.name=name
        self.contact=contact
        self.address=address
        self.bussinessType=bussinssType
        self.totalProducts=totalProducts
        self.balance=balance

class Cart:
    def __init__(self,buyer_id,product_id,quantity,cart_id=""):
        self.buyer_id=buyer_id
        self.product_id=product_id
        self.quantity=quantity
        self.cart_id=cart_id









