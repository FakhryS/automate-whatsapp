from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient(
    "mongodb+srv://Fakhry:fakhry@cluster0.idjuj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["fakhry"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if not bool(user):
        res.message("Hi Tester, thanks for contacting *The Red Velvet*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* "
                    "\n 4️⃣ ""To get our *address 99*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response 99")
            return str(res)

        if option == 1:
            res.message("You can contact us through phone or e-mail.\n\n*Phone*: 991234 56789 \n*E-mail 777* : "
                        "contact@theredvelvet.io")
        elif option == 2:
            res.message("You have entered *ordering mode*.")
            users.update_one({"number": number}, {"$set": {"status": "ordering"}})
            res.message("whatsform.com/tS6zKG")
        elif option == 3:
            res.message("We work from *9 a.m. to 5 p.m*.")

        elif option == 4:
            res.message("We have multiple stores across the city. Our main center is at *4/54, New Delhi*")
        else:
            res.message("Please enter a valid response")
            return str(res)
    elif user["status"] == "ordering":
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "address":
        selected = user["item"]
        res.message("thank you for shopping with us")
        res.message(f"Your order for {selected} has been received and will be delivered within an hour ")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "ordered":
        res.message("Hi, thanks for contacting again.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* "
                    "\n 4️⃣ " "To get our *address*")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
