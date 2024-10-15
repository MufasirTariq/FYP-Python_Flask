from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_mail import Mail, Message
from database import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from database.models import Admin, Menu, MenuFastFood, MenuDeals, Orders, Reservation, Feedback, DailyBlog, PreDeals

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {"host": "mongodb://localhost:27017/TheVenue"}
db.initialize_db(app)

app.secret_key = 'encrypted'
app.config['SESSION_TYPE'] = "filesystem"
app.config['SESSION_PERMANENT'] = False
Session(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mufasirtariq@gmail.com'  # Enter Gmail email
app.config['MAIL_PASSWORD'] = '()cozykme13'  # Enter password

mail = Mail(app)


@app.route("/")
def index():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Overview Settings
        menuItems = Menu.objects().count()
        menuffItems = MenuFastFood.objects().count()
        totalMenuItems = menuItems + menuffItems

        totalRes = Reservation.objects().count()
        totalFeedback = Feedback.objects.filter(comfeed='feedback').count()
        totalComplain = Feedback.objects.filter(comfeed='complain').count()
        totalFeedComp = Feedback.objects().count()

        totalOrders = Orders.objects().count()
        orderBill = Orders.objects()
        totalOrdersBill = 0
        for ob in orderBill:
            totalOrdersBill = totalOrdersBill + ob.bill

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        return render_template("index.html", username=un, email=em, dp="static/images/" + img,
                               admin_id=admin_id, totalMenuItems=totalMenuItems, totalOrders=totalOrders,
                               reservations=totalRes, totalOrdersBill=totalOrdersBill, totalFeedback=totalFeedback,
                               totalComplain=totalComplain, totalFeedComp=totalFeedComp,
                               notiData=notiData, order=order)
    else:
        return render_template("login.html")


@app.route("/ordertable")
def ordertable():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        orderDetails = Orders.objects()
        orderDetailsList = []
        for od in orderDetails:
            tempList = [od.name, od.paymethod, od.items, od.bill, od.date, od.time]
            orderDetailsList.append(tempList)

        customerDetails = Orders.objects()
        customerDetailsList = []
        for od in customerDetails:
            tempList = [od.name, od.email, od.address, od.area, od.phone]
            customerDetailsList.append(tempList)

    return render_template("ordertable.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                           notiData=notiData, order=order, orderDetailsList=orderDetailsList,
                           customerDetailsList=customerDetailsList)


@app.route("/reservation")
def reservation():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        # tableData
        resDetails = Reservation.objects.filter(status='Conflict')

        resDetailsList = []
        for c in resDetails:
            tempList = [c.id, c.fname, c.resDate, c.resTime, c.people, c.specialReq, c.email, c.phone, c.date, c.time, c.status]
            resDetailsList.append(tempList)

        customerDetails = Reservation.objects.filter(status='Accepted')
        customerDetailsList = []
        for od in customerDetails:
            tempList = [od.id, od.fname, od.resDate, od.resTime, od.people, od.specialReq, od.email, od.phone, od.date, od.time, od.status]
            customerDetailsList.append(tempList)

    return render_template("reservation.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                           notiData=notiData, order=order, resDetailsList=resDetailsList,
                           customerDetailsList=customerDetailsList)


@app.route('/resAccepted/<id>', methods=['PUT'])
def acceptReservation(id):
    x = Reservation.objects(id=id).update(status='Accepted')
    res = {'res': 'Accepted'}
    return jsonify(res)


@app.route('/resRejected/<id>', methods=['PUT'])
def rejectReservation(id):
    print(id)
    x = Reservation.objects(id=id).update(status='Rejected')
    cus = Reservation.objects.get(id=id)
    email = cus.email
    res = {'res': 'Rejected', 'email': email}
    return jsonify(res)


@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.form.to_dict()
    email = data['email']
    message_body = data['reason']
    subject = "Reservation Rejected"
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=email)
    msg.body = message_body
    try:
        mail.send(msg)
        res = {'result': 'Mail sent Successfully'}
        return jsonify(res)
    except Exception as e:
        return 'Failed to send email. Error: {}'.format(str(e))


@app.route("/menu")
def form():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        # DataTable Data
        mmData = Menu.objects()
        mmList = []
        for m in mmData:
            tempList = [m.id, m.name, m.price, m.details, m.type, m.date]
            mmList.append(tempList)

        ffData = MenuFastFood.objects()
        ffList = []
        for f in ffData:
            tempList = [f.id, f.name, f.price, f.details, f.type, f.date]
            ffList.append(tempList)

        dmData = MenuDeals.objects()
        dmList = []
        for d in dmData:
            tempList = [d.id, d.name, d.price, d.details, d.type, d.date, d.discount, d.disPrice]
            dmList.append(tempList)

        x = PreDeals.objects()
        PreDealsList = []
        for i in x:
            temp = [i.id, i.name, i.price]
            PreDealsList.append(temp)

    return render_template("menu.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                           notiData=notiData, order=order, main_menu=mmList, fast_food=ffList, deals_menu=dmList, PreDealsList=PreDealsList)


@app.route('/addToMainMenu', methods=['POST'])
def addToMainMenu():
    data = request.form.to_dict()
    date = datetime.now().date()
    x = Menu(name=data['name'], price=data['price'], details=data['details'], type=data['type'], date=str(date)).save()
    res = {'mmID': str(x.id)}
    return jsonify(res)


@app.route('/deletemm/<id>', methods=['DELETE'])
def deletemm(id):
    Menu.objects(id=id).delete()
    res = {'res': 'Deleted'}
    return jsonify(res)


@app.route('/updateMainMenu/<id>', methods=['PUT'])
def updateMainMenu(id):
    data = request.form.to_dict()
    date = datetime.now().date()
    print(id)
    x = Menu.objects(id=id).update(name=data['name'], price=data['price'], details=data['details'], type=data['type'],
                                   date=str(date))
    return jsonify('Updated')


@app.route('/addToFastFood', methods=['POST'])
def addToFastFood():
    data = request.form.to_dict()
    date = datetime.now().date()
    x = MenuFastFood(name=data['name'], price=data['price'], details=data['details'], type=data['type'],
                     date=str(date)).save()
    res = {'ffID': str(x.id)}
    return jsonify(res)


@app.route('/deleteff/<id>', methods=['DELETE'])
def deleteff(id):
    MenuFastFood.objects(id=id).delete()
    res = {'res': 'Deleted'}
    return jsonify(res)


@app.route('/updateFastFood/<id>', methods=['PUT'])
def updateFastFood(id):
    data = request.form.to_dict()
    date = datetime.now().date()
    x = MenuFastFood.objects(id=id).update(name=data['name'], price=data['price'], details=data['details'],
                                           type=data['type'], date=str(date))
    return jsonify('Updated')

@app.route('/preDealDetails', methods=['POST'])
def preDealDetails():
    data = request.form.to_dict()
    x = PreDeals(name=data['name'], price=data['price']).save()

    y = PreDeals.objects()
    total = 0
    nameList =[]
    for i in y:
        total = total + int(i.price)
        nameList.append(i.name)

    res = {"total": total, 'nameList': nameList}
    return jsonify(res)

@app.route('/deletePreDealItem/<id>', methods=['DELETE'])
def deletePreDealItem(id):
    PreDeals.objects(id=id).delete()
    y = PreDeals.objects()
    total = 0
    for i in y:
        total = total + int(i.price)
    return jsonify(total)


@app.route('/addToDeals', methods=['POST'])
def addToDeals():
    data = request.form.to_dict()
    y = PreDeals.objects()
    nameList = []
    for i in y:
        nameList.append(i.name)

    details = ', '.join(nameList)

    date = datetime.now().date()
    x = MenuDeals(name=data['name'], price=data['price'], details=details, type=data['type'],
                  date=str(date), discount=data['discount'], disPrice=data['disPrice']).save()

    PreDeals.objects.delete()
    res = {'dmID': str(x.id)}
    return jsonify(res)


@app.route('/deletedeals/<id>', methods=['DELETE'])
def deletedeals(id):
    MenuDeals.objects(id=id).delete()
    res = {'res': 'Deleted'}
    return jsonify(res)


@app.route('/updateDeals/<id>', methods=['PUT'])
def updateDeals(id):
    data = request.form.to_dict()
    date = datetime.now().date()
    print(id)
    x = MenuDeals.objects(id=id).update(name=data['name'], price=data['price'], details=data['details'],
                                        type=data['type'],
                                        date=str(date))
    return jsonify('Updated')


@app.route("/loginAdminAccount")
def login():
    return render_template("login.html")


@app.route("/adminLoginForm", methods=["POST"])
def loginForm():
    formData = request.form.to_dict()
    em = formData["email"]
    ps = formData["password"]
    print(em, ps)
    action = Admin.objects.get(email=em, password=ps)
    session["admin_id"] = action.id
    return jsonify("Successful")


@app.route("/registerAdminAccount")
def register():
    return render_template("register.html")


@app.route("/adminRegisterForm", methods=["POST"])
def registerFrom():
    formdata = request.form.to_dict()
    image = request.files['image']
    filename = secure_filename(image.filename)
    filepath = os.path.join("static/images", filename)
    image.save(filepath)
    admin = Admin(username=formdata["username"], password=formdata["password"], email=formdata["email"],
                  phone=formdata["phone"], image=filename).save()
    res = {"cus_id": str(admin.id)}
    return jsonify(res)


@app.route("/deleteAdminProfile/<id>", methods=["DELETE"])
def deleteAdminProfile(id):
    Admin.objects(id=id).delete()
    session.clear()
    return jsonify("Deleted")


@app.route("/updateAdminAccount")
def update():
    return render_template("update.html")


@app.route("/blog")
def blog():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        # blog-Data
        blog = DailyBlog.objects()
        blogs = []
        for b in blog:
            temp = [b.id, b.date, b.image, b.about, b.reviewer, b.type, b.react, b.description]
            blogs.append(temp)

        return render_template("blog.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                               notiData=notiData, order=order, blogs=blogs)


@app.route('/deleteBlog/<id>', methods=['DELETE'])
def deleteBlog(id):
    DailyBlog.objects(id=id).delete()
    return jsonify("Blog Deleted")


@app.route('/uploadBlog', methods=['POST'])
def uploadBlog():
    data = request.form.to_dict()
    date = datetime.now().date()
    image = request.files['image']
    filename = secure_filename(image.filename)
    filepath = os.path.join("static/images/blogs/", filename)
    image.save(filepath)
    print("2.", data)

    blogUpload = DailyBlog(date=str(date), image=filename, about=data['about'], reviewer=data['reviewer'],
                           type=data['type'],
                           react=data['react'], description=data['description']).save()

    res = {'blog_id': str(blogUpload.id)}
    return jsonify(res)


@app.route('/updateBlog/<id>', methods=['PUT'])
def updateBlog(id):
    data = request.form.to_dict()
    date = datetime.now().date()
    image = request.files['image']
    filename = secure_filename(image.filename)
    filepath = os.path.join("static/images/blogs/", filename)
    image.save(filepath)

    blogUpload = DailyBlog.objects(id=id).update(date=str(date), image=filename, about=data['about'],
                                                 reviewer=data['reviewer'],
                                                 type=data['type'], react=data['react'],
                                                 description=data['description'])

    return jsonify("updated")

@app.route("/feedback")
def feedback():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

        # Feedback List
        fbData = Feedback.objects(comfeed='feedback')
        feedbackList = []
        for f in fbData:
            temp = [f.name, f.email, f.phone, f.about, f.info, f.date, f.time, f.id, f.comfeed]
            feedbackList.append(temp)

        # Complain List
        cpData = Feedback.objects(comfeed='complain')
        complainList = []
        for c in cpData:
            temp = [c.name, c.email, c.phone, c.about, c.info, c.date, c.time, c.id, c.comfeed]
            complainList.append(temp)

        return render_template("feedback.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                               notiData=notiData, order=order, feedbackList=feedbackList, complainList=complainList)

@app.route('/deleteFeedback/<id>', methods=['DELETE'])
def deleteFeedback(id):
    Feedback.objects(id=id).delete()
    print(id)
    return jsonify("Deleted")

@app.route("/staff")
def staff():
    if session.get("admin_id") is not None:
        admin_id = session["admin_id"]
        adminData = Admin.objects.get(id=admin_id)
        un = adminData.username
        em = adminData.email
        pw = adminData.password
        ph = adminData.phone
        img = adminData.image

        # Top Taskbar
        data = Feedback.objects()
        notiData = []
        date = str(datetime.now().date())
        for d in data:
            if d.date == date:
                dataList = [d.name, d.comfeed, d.date, d.time]
                notiData.append(dataList)

        OrderData = Orders.objects()
        order = []
        date = str(datetime.now().date())
        for o in OrderData[:5]:
            if o.date == date:
                dataList = [o.name, o.phone, o.date, o.time]
                order.append(dataList)

    return render_template("staff.html", username=un, email=em, dp="static/images/" + img, admin_id=admin_id,
                               notiData=notiData, order=order)

@app.route("/inbox")
def inbox():
    return render_template("inbox.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


if __name__ == "__main__":
    app.run()
