from flask import Flask, request, render_template, jsonify, session, redirect
from flask_session import Session
import stripe
from database import db
from database.models import Menu, DailyBlog, MenuFastFood, MenuDeals, addCart, Orders, Reservation,  Feedback
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {"host": "mongodb://localhost:27017/TheVenue"}
db.initialize_db(app)
app.secret_key = 'encrypted'
app.config['SESSION_TYPE'] = "filesystem"
app.config['SESSION_PERMANENT'] = False
Session(app)


@app.route("/")
def index():
    blogData = DailyBlog.objects()
    blogItems = []
    for b in blogData:
        item_list = [b.date, b.image, b.about, b.reviewer, b.type, b.react, b.description]
        blogItems.append(item_list)
    return render_template("index.html", blogs=blogItems)

@app.route("/test")
def test():
    data = Feedback.objects()
    FeedbackList = []
    for f in data:
        temp = [f.id, f.name, f.about, f.comfeed,f.date, f.info]
        FeedbackList.append(temp)

    return render_template("Test.html", FeedbackList=FeedbackList)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/getCartItems", methods=['GET'])
def GEtcartItems():
    CartData = addCart.objects()
    cartItems = []
    for c in CartData:
        item_list = [str(c.id), c.name, c.price, c.details, c.type]
        cartItems.append(item_list)
    return jsonify(cartItems)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/reservation', methods=['POST'])
def reservation():
    data = request.form.to_dict()
    try:
        checkReservation = Reservation.objects.get(resDate=data['resDate'], resTime=data['resTime'])
        date = datetime.now().date()
        time = datetime.now().strftime("%H:%M")
        x = Reservation(fname=data['fname'], lname=data['lname'], email=data['email'], phone=data['phone'],
                        resDate=data['resDate'], resTime=data['resTime'], people=data['people'],
                        specialReq=data['specialReq'], time=time, date=str(date), status='Conflict').save()

        res = {'msg': 'Exist'}
        return jsonify(res)

    except Reservation.DoesNotExist:
        date = datetime.now().date()
        time = datetime.now().strftime("%H:%M")
        x = Reservation(fname=data['fname'], lname=data['lname'], email=data['email'], phone=data['phone'],
                        resDate=data['resDate'], resTime=data['resTime'], people=data['people'],
                        specialReq=data['specialReq'], time=time, date=str(date), status='Accepted').save()
        return jsonify(data)


@app.route("/elements")
def elements():
    CartData = addCart.objects()
    cartItems = []
    total = 0
    for c in CartData:
        item_list = [str(c.id), c.name, c.price, c.details, c.type]
        total = total + int(c.price)
        cartItems.append(item_list)
    print(total)
    return render_template("elements.html", cart=cartItems, total=total)


@app.route('/deleteItemFromCart/<id>', methods=['DELETE'])
def deleteItemCart(id):
    addCart.objects(id=id).delete()
    return jsonify("Deleted")


@app.route("/ordercomplete",methods=['POST'])
def ordercomplete():
    data = request.form.to_dict()
    CartData = addCart.objects()
    items = ""
    total = 0
    for c in CartData:
        total = total + int(c.price)
    for c in CartData:
        items = c.name + " / " + items

    date = datetime.now().date()
    time = datetime.now().strftime("%H:%M")

    order = Orders(name=data["name"], email=data["email"], address=data["address"], area=data["area"],
                   paymethod=data["payMethod"], phone=data["phone"], bill=total, items=items,
                   time=time, date=str(date)).save()

    addCart.objects.delete()
    res = {"order_id": str(order.id)}
    return jsonify(res)


@app.route("/menu")
def menu():
    # Resrtraunt Special Menu
    mainData = Menu.objects(type="main")
    mainItems = []
    for m in mainData:
        item_list = [m.name, m.price, m.type, m.details]
        mainItems.append(item_list)

    staterData = Menu.objects(type="stater")
    staterItems = []
    for s in staterData:
        item_list = [s.name, s.price, s.type, s.details]
        staterItems.append(item_list)

    desertData = Menu.objects(type="dessert")
    desertItems = []
    for d in desertData:
        item_list = [d.name, d.price, d.type, d.details]
        desertItems.append(item_list)

    # Fast Food Menu
    pizzaData = MenuFastFood.objects(type="pizza")
    pizzaItems = []
    for p in pizzaData:
        item_list = [p.name, p.price, p.type, p.details]
        pizzaItems.append(item_list)

    burgerData = MenuFastFood.objects(type="burger")
    burgerItems = []
    for b in burgerData:
        item_list = [b.name, b.price, b.type, b.details]
        burgerItems.append(item_list)

    othersData = MenuFastFood.objects(type="other")
    otherItems = []
    for o in othersData:
        item_list = [o.name, o.price, o.type, o.details]
        otherItems.append(item_list)

    # # Deal Menu
    midNightData = MenuDeals.objects(type="midnight")
    mdItems = []
    for m in midNightData:
        item_list = [m.name, m.price, m.type, m.details, m.disPrice, m.discount]
        mdItems.append(item_list)

    occData = MenuDeals.objects(type="occasion")
    occItems = []
    for o in occData:
        item_list = [o.name, o.price, o.type, o.details, o.disPrice, o.discount]
        occItems.append(item_list)

    specialData = MenuDeals.objects(type="special")
    specialItems = []
    for s in specialData:
        item_list = [s.name, s.price, s.type, s.details, s.disPrice, s.discount]
        specialItems.append(item_list)

    CartData = addCart.objects()
    cartItems = []
    for c in CartData:
        item_list = [str(c.id), c.name, c.price, c.details, c.type]
        cartItems.append(item_list)

    return render_template("menu.html", main=mainItems, stater=staterItems, desert=desertItems,
                               pizza=pizzaItems, burger=burgerItems, others=otherItems,
                               midnight=mdItems, occasion=occItems, special=specialItems, cartItems=cartItems)


@app.route('/searchMenuItems/<target>', methods=['GET'])
def searchMenuItems(target):
    target = target.lower()
    main_menu_results = Menu.objects(name__icontains=target)
    fast_food_results = MenuFastFood.objects(name__icontains=target)
    deals_results = MenuDeals.objects(name__icontains=target)

    MMresults = [item.to_json() for item in main_menu_results]
    FFresults = [item.to_json() for item in fast_food_results]
    Dresults = [item.to_json() for item in deals_results]

    return jsonify(MMresults, FFresults, Dresults)


@app.route('/addCart', methods=["POST"])
def addCartFunc():
    order = request.form.to_dict()
    n = addCart(name=order["name"], price=order["price"], details=order["details"], type=order["type"]).save()
    res = {"cart_id": str(n.id)}
    return jsonify(res)

@app.route("/feedback")
def feedback():
    data = Feedback.objects()
    FeedbackList = []
    for f in data:
        temp = [f.id, f.name, f.about, f.comfeed, f.date, f.info]
        FeedbackList.append(temp)
    return render_template("blog.html", FeedbackList=FeedbackList)


@app.route('/complain', methods=['POST'])
def complain():
    data = request.form.to_dict()
    date = str(datetime.now().date())
    time = datetime.now().strftime('%H:%M')

    x = Feedback(name=data['name'], email=data['email'], phone=data['phone'],
                 about=data['about'], comfeed=data['comfeed'], info=data['info'], date=date, time=time).save()
    res = {'comfeed': data['comfeed'], 'about': data['about']}
    return jsonify(res)


if __name__ == "__main__":
    app.run(port=5001)
