

from view import *


import pymysql
class eMartmodel:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.connection=None
        try:
            self.connection=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            print("Connected Successfully")
        except Exception as e:
            print("There is error While connecting databases")
    def isUserAlreadyExist(self,email):
        sql="select * from users where email=%s;"
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                cursor.execute(sql,email)
                if(cursor.fetchone()!=None):
                    return True
                else:
                    return False
        except Exception as e:
            print("Something went wrong")
        finally:
            print("cursor closed")
            cursor.close()

    def isUser(self,user):
        if(self.isUserAlreadyExist(user.email)):
            sql="select * from users where email=%s and password=%s;"
            try:
                if self.connection!=None:
                    cursor = self.connection.cursor()
                    data=(user.email,user.password)
                    cursor.execute(sql, data)
                    result=cursor.fetchone()
                    if result!=None:
                        if result[3]=="admin":
                            return result
                        else:
                            if result[3]=="buyer":
                                sql1 = "select id from buyer where userid=%s;"
                            elif result[3]=="seller":
                                sql1 = "select id from seller where userid=%s;"
                            cursor.execute(sql1,result[0])
                            r=cursor.fetchone()
                            res=list(result)
                            res.append(r[0])
                            return res
                    else:
                        return None
            except Exception as e:
                print("Something Went Wrong in user")
            finally:
                print("final calls")

    def addUser(self, user,name):
        if (not self.isUserAlreadyExist(user.email)):
            sql = "INSERT INTO `users` (`email`, `password`, `status`) VALUES (%s,%s,%s);"
            try:
                if self.connection != None:
                    cursor = self.connection.cursor()
                    data = (user.email, user.password, user.type)
                    cursor.execute(sql, data)
                    self.connection.commit()
                    if user.type=="seller":
                        sql2="insert into seller (`userid`,`name`,`image`) values (%s,%s,'profile.png');"
                    else:
                        sql2="insert into buyer (`userid`,`name`,`image`) values(%s,%s,'profile.png');"
                    cursor.execute("select max(id) from users")
                    arg=(cursor.fetchone(),name)
                    cursor.execute(sql2,arg)
                    self.connection.commit()
                    return True
                else:
                    return False
            except Exception as e:
                print("Something Went Wrong in user",e)
                return False
            finally:
                print("final calls")

    def getBuyerRegData(self,userid):
        sql="select * from buyer where `userid`=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, userid)
                data=cursor.fetchone()
                buyer=Buyer(data[2],data[3],data[4],data[5],data[6],data[8],data[7])
                return buyer
        except Exception as e:
            print("Something Went Wrong in Getting Buyers Registing Data", e)
            return False
        finally:
            print("final calls")

    def registerBuyer(self,regdata,userid):
        sql="UPDATE `buyer` SET name=%s, `contact` = %s, `s_email` = %s, `c_address` = %s, p_address=%s,`image`=%s ,balance=%s  WHERE `userid` = %s;"
        sql1="update users set `profileStatus`='1' where `id`=%s ;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                data = (regdata.name,regdata.contact,regdata.s_email,regdata.c_address,regdata.p_address,regdata.image,regdata.balance,userid)
                cursor.execute(sql, data)
                self.connection.commit()
                cursor.execute(sql1,userid)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Something Went Wrong in Registing user", e)
            return False
        finally:
            print("final calls")

    def registerSeller(self,regdata,userid):
        sql = "UPDATE `seller` SET `name`=%s,`contact`=%s,`address` = %s, `business type` = %s,`image`=%s WHERE `seller`.`id` = %s;"
        sql1 = "update users set `profileStatus`='1' where `id`=%s ;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                data = (regdata.name, regdata.contact, regdata.address, regdata.bussinessType, regdata.image, userid)
                cursor.execute(sql, data)
                self.connection.commit()
                cursor.execute(sql1, userid)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Something Went Wrong in Registing user", e)
            return False
        finally:
            print("final calls")

    def addProduct(self,product):
        sql="INSERT INTO `product` (`name`, `price`, `discription`, `discount`, `catagory`, `seller_id`, `quantity`, `entry_date`,`image`) VALUES (%s, %s, %s, %s, %s, %s, %s, sysdate(),%s);"
        s = "select max(id) from product;"
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                cursor.execute(s)
                maxid=cursor.fetchone()[0]
                imgname=str(int(maxid) + 1) + "." + product.image
                args=(product.name,product.price,product.description,product.discount,product.catagory,product.seller_id,product.quantity,imgname)
                if cursor.execute(sql,args):
                    self.connection.commit()
                    return str(imgname)
                else:
                    return False
        except Exception as e:
            print("Something went wrong in adding")
        finally:
            print("cursor closed")
            cursor.close()

    def getProducts(self,catagory="",limit='0'):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                if catagory == "":
                    if limit=='0':
                        sql = "select * from product;"
                        cursor.execute(sql)
                    else:
                        sql = "select * from product order by id desc limit %s;"
                        cursor.execute(sql,limit)
                else:
                    if limit=='0':
                        sql = "select * from product where `catagory`=%s;"
                        cursor.execute(sql,catagory)
                    else:
                        sql = "select * from product where `catagory`=%s order by id desc limit %s;"
                        argu=(catagory,limit)
                        cursor.execute(sql, argu)
                result=cursor.fetchall()
                print(result)
                data=[]
                for x in result:
                    data.append({'id':x[0],'name':x[1],'price':x[2],'discription':x[3],'discount':x[4],'catagory':x[5],'seller_id':x[6],'quantity':x[7],'entry_date':x[8],'rating':x[9],'image':x[10]})
                return data
        except Exception as e:
            print("Something went wrong in getting Products: ",e)
        finally:
            print("cursor closed")
            cursor.close()

    def getproducts(self,sid=None):
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                if sid == None:
                    sql = "select id,name,price,catagory,seller_id,entry_date from product;"
                    cursor.execute(sql)
                else:
                    sql = "select id,name,price,catagory,seller_id,entry_date from product where seller_id=%s;"
                    cursor.execute(sql,sid)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("Something went wrong in getting Products: ",e)
        finally:
            print("cursor closed")
            cursor.close()

    def getsellerproducts(self,sid):
        sql = "select id,name,price,catagory,shipement_charges,entry_date from product where seller_id=%s;"
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                cursor.execute(sql,sid)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("Something went wrong in getting Products: ",e)
        finally:
            print("cursor closed")
            cursor.close()


    def delProduct(self,p_id,s_id):
        sql = "delete from product where id=%s;"
        sql1="update seller set totalproducts=(select totalproducts-1 from product where id=%s) WHERE id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, p_id)
                self.connection.commit()
                cursor.execute(sql1, s_id)
                self.connection.commit()
                return True
        except Exception as e:
            print("Something went wrong in Deleting Product", e)
        finally:
            print("cursor closed")
            cursor.close()

    def isAlreadyAddedToCart(self,buyer_id,product_id):
        sql = "select cart_id,quantity from cart where buyer_id=%s and product_id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                argu = (buyer_id, product_id)
                cursor.execute(sql, argu)
                result=cursor.fetchone()
                return result
        except Exception as e:
            print("Something went wrong in checking to Cart", e)
        finally:
            print("cursor closed")
            cursor.close()

    def addToCart(self,cart):
        cartid=self.isAlreadyAddedToCart(cart.buyer_id, cart.product_id)
        if  cartid!= None:
            print(cartid[0])
            argu = (str(int(cartid[1])+int(cart.quantity)), cartid[0])
            sql="update cart set quantity=%s where cart_id=%s;"
        else:
            argu = (cart.buyer_id, cart.product_id, cart.quantity)
            sql="insert into cart (`buyer_id`,`product_id`,`quantity`,`date`) values (%s,%s,%s,sysdate());"
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                cursor.execute(sql,argu)
                if self.connection.commit():
                    return True
                else:
                    return False
        except Exception as e:
            print("Something went wrong in adding to Cart",e)
        finally:
            print("cursor closed")
            cursor.close()



    def getCart(self,buyerId):
        sql = "select * from cart where buyer_id=%s;"
        sql1= "select * from product where id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, buyerId)
                cartDetails=cursor.fetchall()
                cart=[]
                for x in cartDetails:
                    cursor.execute(sql1, x[2])
                    pro=cursor.fetchone()
                    c={"cart":Cart(x[1],x[2],x[3],x[0]),"product":{'id':pro[0],'name':pro[1],'price':pro[2],'image':pro[10],'discount':pro[4],'deliver':pro[11]}}
                    cart.append(c)
                return cart
            else:
                return False
        except Exception as e:
            print("Something went wrong in Getting Cart", e)
        finally:
            print("cursor closed")
            cursor.close()

    def clearCart(self,i):
        sql = "DELETE FROM `cart` WHERE buyer_id= %s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, i)
                self.connection.commit()
                return True

            else:
                return False
        except Exception as e:
            print("Something went wrong in Clearing Cart", e)
        finally:
            print("cursor closed")
            cursor.close()


    def updateCart(self,dta):
        sql = "update cart set quantity=%s where cart_id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                for x in dta:
                    if x['quantity']=='0':
                        sql1="delete from cart where cart_id=%s;"
                        cursor.execute(sql1,x['cart_id'])
                    else:
                        argu=(x['quantity'],x['cart_id'])
                        cursor.execute(sql, argu)
                    self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Something went wrong in Clearing Cart", e)
        finally:
            print("cursor closed")
            cursor.close()

    def getUsers(self,type):
        if type=="buyer":
            sql = "select u.id,b.name,u.email,u.profileStatus from users u, buyer b where u.status='buyer' and b.userid=u.id;"
        elif type=="seller":
            sql = "select u.id,b.name,u.email,u.profileStatus,b.balance,b.totalproducts from users u, seller b where u.status='seller' and b.userid=u.id;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql)
                data=cursor.fetchall()
                return data
        except Exception as e:
            print("Something went wrong in Getting users", e)
        finally:
            print("cursor closed")
            cursor.close()


    def delUser(self,id):
        sql="delete from buyer where userid=%s;"
        sql1="delete from users where id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql,id)
                self.connection.commit()
                cursor.execute(sql1,id)
                self.connection.commit()
                return True
        except Exception as e:
            print("Something went wrong in Getting users", e)
        finally:
            print("cursor closed")
            cursor.close()

    def getTotals(self,id=0):

        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                if id != '0':
                    sql = "select count(*) from `order` where seller_id=%s"
                    sql1 = "select count(*) from `product` where seller_id=%s"
                    cursor.execute(sql,id)
                    users = cursor.fetchone()
                    cursor.execute(sql1,id)
                    products = cursor.fetchone()
                    return {'orders': users[0], 'products': products[0]}
                else:
                    sql = "select count(*) from users where status='buyer'"
                    sql1 = "select count(*) from users where status='seller'"
                    sql2 = "select count(*) from product"
                    cursor.execute(sql)
                    users=cursor.fetchone()
                    cursor.execute(sql1)
                    sellers = cursor.fetchone()
                    cursor.execute(sql2)
                    products = cursor.fetchone()
                    return {'user':users[0],'seller':sellers[0],'product':products[0]}
        except Exception as e:
            print("Something went wrong in Getting Totals", e)
        finally:
            print("cursor closed")
            cursor.close()


    def addOrder(self,id):
        sql="INSERT INTO `order` (`product_id`, `buyer_id`,`seller_id`, `order_date`, `quantity`) VALUES (%s,%s,%s,sysdate(),%s); "
        sql1="select c.buyer_id,c.product_id,c.quantity,p.seller_id from cart c,product p where c.buyer_id=%s and p.id=c.product_id;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql1,id)
                pro=cursor.fetchall()
                print(pro)
                for x in pro:
                    argu=(str(x[1]),str(x[0]),str(x[3]),str(x[2]))
                    cursor.execute(sql,argu)
                    self.connection.commit()
                return True
        except Exception as e:
            print("Something went wrong in Adding Order", e)
        finally:
            print("cursor closed")
            cursor.close()

    def deliverd(self,id):
        sql="update `order` set `shipement`='deliverd' where id=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, id)
                self.connection.commit()
                return True
        except Exception as e:
            print("Something went wrong in getting Order", e)
        finally:
            print("cursor closed")
            cursor.close()



    def getorder(self,type,id):
        if type=="buyer":
            sql="select p.name,o.quantity,o.shipement from `order` o,product p where o.buyer_id=%s and o.product_id=p.id;"
        else:
            sql = "select o.id,p.name,u.email,b.name,b.c_address,o.shipement,o.quantity from `order` o, `product` p , `buyer` b , `users` u where o.seller_id=%s and o.product_id=p.id and o.buyer_id=b.userid and u.id=b.userid;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, id)
                result=cursor.fetchall()
                return result
        except Exception as e:
            print("Something went wrong in getting Order", e)
        finally:
            print("cursor closed")
            cursor.close()

    def getSellerRegData(self,id):
        sql = "select * from seller where `userid`=%s;"
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, id)
                data = cursor.fetchone()
                seller = Seller(data[2], data[3], data[4], data[5], data[6], data[8], data[7])
                return seller
        except Exception as e:
            print("Something Went Wrong in Getting seller Registing Data", e)
            return False
        finally:
            print("final calls")

    def getlogin(self,id,type):
        if type=="buyer":
            sql='select name,image from buyer where userid=%s;'
        elif type=="seller":
            sql = 'select name,image from seller where userid=%s;'
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(sql, id)
                result=cursor.fetchone()
                return result
        except Exception as e:
            print("Something went wrong in getting login info", e)
        finally:
            print("cursor closed")
            cursor.close()



