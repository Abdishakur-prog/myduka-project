from flask import Flask,render_template,request
import psycopg2
conn=psycopg2.connect(user="postgres",password="1234",host="localhost",database="myduka")
cur=conn.cursor()
print("database connected successfully")


app=Flask(__name__)

@app.route("/")

def index():
    name="mohamed"
    return render_template("index.html", myname=name)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact us")
def contact():
    return render_template("contact.html")

@app.route("/products",methods=["GET","POST"])
def fetchProducts():
    if request.method=="GET":
        cur.execute("select * from products;")
        products=cur.fetchall()
        return render_template("products.html", myproducts=products)
    else:
        name=request.form["pname"]
        buying_price=request.form["bp"]
        selling_price=request.form["sp"]
        stock_quantity=request.form["st"]
        print(name,buying_price,selling_price,stock_quantity)
        return "products added succesfully"


app.run()

