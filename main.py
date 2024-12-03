from flask import Flask,render_template
import psycopg2
conn=psycopg2.connect(user="postgres",password="1234",host="localhost",database="myduka")
cur=conn.cursor()
print("database connected successfully")


app=Flask(__name__)

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact us")
def contact():
    return render_template("contact.html")

@app.route("/products")
def fetchProducts():
    cur.execute("select * from products;")
    products=cur.fetchall()
    return render_template("products.html")





app.run()

