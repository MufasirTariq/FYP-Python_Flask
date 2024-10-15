from database.db import db


class Menu(db.Document):
    name = db.StringField(required=True)
    price = db.StringField(required=True)
    details = db.StringField(required=True)
    type = db.StringField(required=True)  # main, starter, desert
    date = db.StringField(required=True)
class MenuFastFood(db.Document):
    name = db.StringField(required=True)
    price = db.StringField(required=True)
    details = db.StringField(required=True)
    type = db.StringField(required=True)  # pizza, Bur gers, Otherrs
    date = db.StringField(required=True)
class MenuDeals(db.Document):
    name = db.StringField(required=True)
    price = db.StringField(required=True)
    details = db.StringField(required=True)
    type = db.StringField(required=True)  # Midnight, Occassionaly, Special
    date = db.StringField(required=True)
    disPrice = db.StringField(required=True)
    discount = db.StringField(required=True)

class DailyBlog(db.Document):
    date = db.StringField(required=True)
    image = db.StringField(required=True)
    about = db.StringField(required=True)
    reviewer = db.StringField(required=True)
    type = db.StringField(required=True)
    react = db.StringField(required=True)
    description = db.StringField(required=True)


class addCart(db.Document):
    name = db.StringField(required=True)
    price = db.StringField(required=True)
    details = db.StringField()
    type = db.StringField()

class Orders(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    address = db.StringField(required=True)
    area = db.StringField(required=True)
    paymethod = db.StringField(required=True)
    phone = db.StringField(required=True)
    items = db.StringField(required=True)
    bill = db.IntField(required=True)
    date = db.StringField(required=True)
    time = db.StringField(required=True)

class Reservation(db.Document):
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    email = db.StringField(required=True)
    phone = db.StringField(required=True)
    resDate = db.StringField(required=True)
    resTime = db.StringField(required=True)
    people = db.StringField(required=True)
    specialReq = db.StringField(required=True)
    date = db.StringField(required=True)
    time = db.StringField(required=True)
    status = db.StringField(required=True)

class Feedback(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    phone = db.StringField(required=True)
    about = db.StringField(required=True)
    comfeed = db.StringField(required=True)
    info = db.StringField(required=True)
    date = db.StringField(required=True)
    time = db.StringField(required=True)

