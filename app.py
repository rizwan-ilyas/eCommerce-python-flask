from cgitb import reset
from itertools import repeat

import requests
from flask import Flask, render_template, request, make_response, url_for, redirect,jsonify
import os
import stripe

from werkzeug.utils import secure_filename

import config
from model import *
from view import *

app = Flask(__name__)
app.config.from_object("config")

stripe_keys = {
  'secret_key': config.secretKey,
  'publishable_key':config.publishKey
}
stripe.api_key = stripe_keys['secret_key']

emartmodel=eMartmodel(config.hostname,config.user,config.password,config.database)


@app.route('/')
def index():
    newArrival=emartmodel.getProducts()
    if 'id' in request.cookies:
        d=emartmodel.getlogin(request.cookies.get('id'),request.cookies.get('type'))
        data=(request.cookies.get('email'),request.cookies.get('type'),d[0],d[1])
    else:
        data=None
    return render_template("index.html",data1=data,data=newArrival)


@app.route('/login')
def login():
    return render_template("login.html",error=None)

@app.route('/login', methods=['POST'])
def loginform():
    user=User(request.form['email'],request.form['password'])
    info=emartmodel.isUser(user)
    if(info!=None):
        response = make_response(redirect('/afterlogin'))
        response.set_cookie("id", str(info[0]))
        response.set_cookie("email", str(info[1]))
        response.set_cookie("type", str(info[3]))
        response.set_cookie("profilestatus", str(info[4]))
        #response.set_cookie("type_id",str(info[5]))
        return response
    else:
        if(emartmodel.isUserAlreadyExist(user.email)):
            return render_template("login.html",error="Password is Incorrect")
        else:
            return render_template("login.html",error="User does not exist")


@app.route('/afterlogin')
def goTo():
    if 'id' in request.cookies:
        if request.cookies.get("type")=="seller":
            if request.cookies.get("profilestatus")=="1":
                return redirect("/seller")
            else:
                return redirect("/registration")
        elif request.cookies.get("type")=="buyer":
            if request.cookies.get("profilestatus")=="1":
                return redirect("/")
            else:
                return redirect("/registration")
        elif request.cookies.get("type")=="admin":
            print("admin")
            return redirect("/admin")
    else:
        return render_template("login.html",error="Something Went Wrong! Please try Again")


@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signupform():
    name=request.form['firstname']+" "+request.form['lastname']
    email=request.form['email']
    if(request.form['password1']==request.form['password2']):
        password=request.form['password1']
        if 'type' in request.form:
            user = User(email, password,request.form["type"])
        else:
            user=User(email,password)
        if emartmodel.addUser(user,name)==True:
            return redirect(url_for("login"))
        else:
            if emartmodel.isUserAlreadyExist(email):
                return render_template("signup.html", error="User Already Exist")
            else:
                return render_template("signup.html",error="Something Went Wrong")
    else:
        return render_template("signup.html",error="Password Does not Match")

@app.route('/addProduct')
def addproduct():
    if ('id' in request.cookies and request.cookies.get("type")=="seller"):
        return render_template("addProduct.html")
    else:
        return redirect(url_for('registration'))


@app.route('/addProduct', methods=["POST"])
def addproductform():
    if('id' in request.cookies):
        if(request.form['sub']=="Add Product Now"):
            name=request.form['name']
            price=request.form['price']
            desc=request.form['description']
            catag=request.form['catagory']
            quantity=request.form['quantity']
            discount=request.form['discount']
            file=request.files['product_image']
            product=Product(name,price,desc,discount,catag,request.cookies.get("id"),quantity,str(file.filename.split('.')[1]))
            e=emartmodel.addProduct(product)
            if e!=False:
                filenam = secure_filename(e)
                file.save(os.path.join("static/upload/products/", filenam))
                return render_template("addProduct.html",error="Inserted")
            else:
                return render_template("addProduct.html",error="something went Wrong Please Try Again")
    else:
        return render_template("login.html",error="You need to login again")


@app.route('/registration')
def registration():
    if ('id' in request.cookies):
        if request.cookies.get("type")=="seller":
            return render_template("seller_reg.html",data=emartmodel.getSellerRegData(str(request.cookies.get('id'))))
        elif request.cookies.get("type")=="buyer":
            return render_template("user.html", data=emartmodel.getBuyerRegData(str(request.cookies.get('id'))))
        return render_template("addProduct.html")
    else:
        return redirect(url_for('login'))

@app.route('/registration', methods=["POST"])
def registrationform():
    if request.cookies.get("type")=="seller":
        name = request.form['fname'] + " " + request.form['lname']
        contact = request.form['ph#']
        address = request.form['address']
        catagory = request.form['b_catagory']
        imag = request.files['imgFile']
        print(imag.filename)
        if imag.filename == "":
            sellerData = Seller(name, contact,address, catagory,0)
        else:
            filenam = secure_filename(str(request.cookies.get('id') + imag.filename.split('.')[1]))
            imag.save(os.path.join("static/upload/profiles/", filenam))
            sellerData = Seller(name, contact,address, catagory,0, filenam)
        if emartmodel.registerSeller(sellerData, request.cookies.get('id')):
            return redirect('/seller')
        else:
            return redirect(url_for("registration"))





    elif request.cookies.get("type")=="buyer":
        name=request.form['fname']+" "+request.form['lname']
        contact=request.form['ph#']
        c_address=request.form['c_address']
        p_address=request.form['p_address']
        s_email=request.form['s_email']
        imag = request.files['imgFile']
        print(imag.filename)
        if imag.filename == "":
            buyerData=Buyer(name,contact,s_email,c_address,p_address)
        else:
            filenam = secure_filename(str(request.cookies.get('id') + imag.filename.split('.')[1]))
            print(imag.filename.split('.')[1])
            imag.save(os.path.join("static/upload/profiles/", filenam))
            buyerData = Buyer(name, contact, s_email, c_address, p_address, filenam)
        if emartmodel.registerBuyer(buyerData,request.cookies.get('id')):
            return redirect('/')
        else:
            return redirect(url_for("registration"))


@app.route("/allProducts")
def allproducts():
    products=emartmodel.getProducts()
    #products=emartmodel.getNewArival()
    return render_template("products.html",data=products)


@app.route('/addToCart/<name>', methods=["GET"])
def addtocart(name):
    if 'id' in request.cookies:
        if request.get_json()!=None:
            print(request.get_json())
            cart = Cart(request.cookies.get('id'), name, request.get_json())
        else:
            cart=Cart(request.cookies.get('id'),name,'1')
        data = {'title': "Add To Cart", 'alert': "Product has been added To Cart Successfully",'redirect':"/"}
        emartmodel.addToCart(cart)
        return render_template("alerts.html",data=data)
    else:
        return render_template("login.html",error="You Need to Login First!")

@app.route('/cart')
def cart():
    if 'id' in request.cookies:
        cart=emartmodel.getCart(request.cookies.get('id'))
        #print(request.cookies.get('id'))
        return render_template("cart.html",data=cart)
    else:
        return render_template("login.html", error="You Need to Login First!")

@app.route('/clearCart')
def clearCart():
    if emartmodel.clearCart(request.cookies.get('id'))==True:
        return redirect(url_for('cart'))
    else:
        return render_template('login.html')

@app.route("/updateCart", methods=["GET","POST"])
def updatecart():
    d=request.get_json()
    if emartmodel.updateCart(d)==True:
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('cart'))

@app.route("/checkout")
def checkout():
    if 'id' in request.cookies:
        cart=emartmodel.getBuyerRegData(request.cookies.get('id'))
        d=emartmodel.getCart(request.cookies.get('id'))
        print(d)
        #print(request.cookies.get('id'))
        return render_template("checkout.html",key=stripe_keys['publishable_key'],cart= d,data=cart)
    else:
        return render_template("login.html", error="You Need to Login First!")


@app.route('/shop')
def shope():
    return render_template("shop-grid-left-sidebar.html")

@app.route('/aboutUs')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route('/charge', methods=['GET','POST'])
def charge():
    if 'id' in request.cookies:
        amount=250
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )

        if emartmodel.addOrder(request.cookies.get('id'))==True:
            emartmodel.clearCart(request.cookies.get('id'))
            data={'title':"Debit Card Payment",'alert': "Payment Done!!",'redirect':'/'}
            return render_template('alerts.html',data=data)
    else:
        return redirect(url_for('/login'))


@app.route('/admin')
def admin():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="admin":
            return render_template("admin.html",totals=emartmodel.getTotals())
        else:
            return redirect('/')
    else:
        return redirect('/login')

@app.route('/adminusers')
def adminuser():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="admin":
            data=emartmodel.getUsers("buyer")
            return jsonify(data)
        else:
            return redirect('/')
    else:
        return redirect('/login')

@app.route('/adminseller')
def adminseller():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="admin":
            data=emartmodel.getUsers("seller")
            return jsonify(data)
        else:
            return redirect('/')
    else:
        return redirect('/login')

@app.route('/adminproducts')
def adminproduct():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="admin":
            data=emartmodel.getproducts()
            return jsonify(data)
        else:
            return redirect('/')
    else:
        return redirect('/login')



@app.route('/delUser',methods=['POST'])
def delUser():
    if emartmodel.delUser(request.get_json())==True:
        return redirect(url_for('/adminusers'))

@app.route('/delProduct',methods=['POST','GET'])
def delProduct():
    ids=request.get_json()
    if emartmodel.delProduct(ids.split('_')[0],ids.split('_')[1])==True:
        return redirect(url_for('/adminproducts'))


@app.route('/order')
def order():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="buyer":
            return render_template("orders.html")
        elif request.cookies.get('type')=="seller":
            return redirect('/seller')
    else:
        return redirect('/login')

@app.route('/orderdata')
def orderdata():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="buyer":
            data = emartmodel.getorder('buyer', request.cookies.get('id'))
            print(data)
            return jsonify(data)
        else:
            return redirect('/')
    else:
        return redirect('/login')


@app.route('/seller')
def seller():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="seller":
            data=emartmodel.getorder("seller",request.cookies.get("id"))
            totals=emartmodel.getTotals(request.cookies.get("id"))
            return render_template("seller.html",total=totals)
        elif request.cookies.get('type')=="buyer":
            return redirect('/order')
    else:
        return redirect('/login')

@app.route('/delivered')
def deliverd():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="buyer":
            data=emartmodel.deliverd(request.get_json())
            print(data)
            if data==True:
                return redirect('/order')
        elif request.cookies.get('type')=="buyer":
            return redirect('/order')
    else:
        return redirect('/login')

@app.route('/sellerorder')
def sellerorder():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="seller":
            data=emartmodel.getorder("seller",request.cookies.get("id"))
            return jsonify(data)

    else:
        return redirect('/login')


@app.route('/sellerproducts')
def sellerOrder():
    if 'id' in request.cookies:
        if request.cookies.get('type')=="seller":
            data=emartmodel.getsellerproducts(request.cookies.get('id'))
            return jsonify(data)
    else:
        return redirect('/login')








@app.route('/logout')
def logout():
    response=make_response(redirect('login'))
    response.delete_cookie('id')
    response.delete_cookie('email')
    response.delete_cookie('type')
    response.delete_cookie('profilestatus')
    return response







if __name__ == '__main__':
    app.run()