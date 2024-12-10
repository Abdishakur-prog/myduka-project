from flask import Flask,render_template,request,redirect
import psycopg2
conn=psycopg2.connect(user="postgres",password="1234",host="localhost",database="myduka")
cur=conn.cursor()
print("database connected successfully")


app=Flask(__name__)
@app.template_filter('strftime')
def format_datetime(value, format="%B %d,%Y"):
    return value.strftime(format)


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
        query="insert into products(name,buying_price,selling_price,stock_quantity) "\
        "values('{}',{},{},{})".format(name,buying_price,selling_price,stock_quantity)
        cur.execute(query)
        conn.commit()
        return redirect("/products")
    
@app.route("/sales",methods=["GET","POST"])
def fetchsales():
    if request.method=="post":
        pname=request.form["pid"]
        quantity=request.form["quantity"]
        query="insert into sales(product_name,quantity,created_at) "\
        "values('{}',{},{})".format(pname,quantity,"now()")
        cur.execute(query)
        conn.commit()
        return redirect("/sales")

    else:
       cur.execute("select * from products")
       conn.commit
       products=cur.fetchall()
       cur.execute("select sales.ID, products.Name, sales.quantity, sales.created_at "\
                    "from sales inner join products on sales.pid = products.id")
       sales=cur.fetchall()
       return render_template("sales.html",mysales=sales,products=products,sales=sales)
    
@app.route("/dashboard")
def d_board():
    cur.execute("select sum(p.selling_price * s.quantity)as sales,\
                s.created_at from sales as s join products as p on p.id=s.pid group by s.created_at")
    daily_sales=cur.fetchall()
    x=[i[1].strftime('%d %m %Y') for i in daily_sales if float(i[0]>60000)]
    y=[float(i[0]) for i in daily_sales if float(i[0]>60000)]
    
    return render_template("dashboard.html",x=x,y=y)

app.run(debug=True)

