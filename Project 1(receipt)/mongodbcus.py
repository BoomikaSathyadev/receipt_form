from flask import Flask
from flask import Flask, jsonify, request, redirect, render_template
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# database
username = quote_plus("boomikasathyadev")
password = quote_plus("Cu4LeKtnaUNUtwYA") 
uri = f"mongodb+srv://boomikasathyadev:Cu4LeKtnaUNUtwYA@cluster0.bgrigtw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
app.config["MONGO_URI"] = uri

# Database name
db_name = "customer"
client = MongoClient(app.config["MONGO_URI"])

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select the database
db = client.get_database(db_name)

# TO STORE THE DATA AND REDIRECT THE PAGE
def bill_number() :
    word = "EDE"
    num = '00'
    result = num.rjust(3,"0")
    a = word + result
    # return a
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    print(today)
    collection = db['bill']
    count = collection.count_documents({"date":today})
    print(count)
    # find = list(collection.find({"date":"2024-06-28"}))
    # print(find)
    c = count + 1
    return f'{a}{c}'

@app.route('/',methods=['GET', 'POST'])
def bill():
    if request.method == 'POST':
        collection = db['bill']
        name = request.form['billname']
        address = request.form['billaddress']
        age = request.form['billage']
        mobile = request.form['billmobile']
        email = request.form['billemail']
        billno = bill_number()
        amount = request.form['billamount']
        date = request.form['billdate']
        data = {'name':name,'address':address,'age':age,'mobile':mobile,'email':email,'billno':billno,'amount':amount,'date':date}
        result = collection.insert_one(data)
        print(result)
        return redirect("/billlist")
    bill_list = [
        {'name':'ak','address':'qwertyui','billno':'EDE0001','amount':'1000','date':'01-01-2024','mobile':'7234567890','age_filter':'20-29'},
        {'name':'bk','address':'qwertyui','billno':'EDE0002','amount':'5000','date':'27-01-2024','mobile':'8827807845','age_filter':'40-49'},
        {'name':'ck','address':'qwertyui','billno':'EDE0003','amount':'15000','date':'15-02-2024','mobile':'9367585759','age_filter':'30-39'},
        {'name':'dk','address':'qwertyui','billno':'EDE0004','amount':'8500','date':'03-03-2024','mobile':'6674547388','age_filter':'50-59'},
    ]
    context = {'bill_list':bill_list,'bill_number':bill_number()}
    return render_template('master/bill.html',context=context)

@app.route('/billlist')
def billList():
    collection = db['bill']
    bill_list = list(collection.find())
    context = {'bill_list':bill_list,'bill_number':bill_number()}
    return render_template('master/billdetails.html',context=context)

# TO DELETE
@app.route('/delete/<document_id>')
def delete_document(document_id):
    collection = db['bill']
    result = collection.delete_one({"_id": ObjectId(document_id)})
    # result = collection.delete_many({"name": document_id})
    if result.deleted_count > 0:
        return jsonify({"status": "success", "deleted_count": result.deleted_count})
    else:
        # return jsonify({"status": "failed", "deleted_count": result.deleted_count})
    # print(result)
        return redirect("/billlist")

# # TO EDIT  - employeedetails.html
@app.route('/billedit/<id>',methods=['GET','POST'])
def billedit(id):
    collection = db['bill']
    if request.method == 'POST':
        collection = db['bill']
        name = request.form['billname']
        address = request.form['billaddress']
        age = request.form['billage']
        mobile = request.form['billmobile']
        email = request.form['billemail']
        amount = request.form['billamount']
        date = request.form['billdate']
        data = {'name':name,'address':address,'age':age,'mobile':mobile,'email':email,'amount':amount,'date':date}
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"status": "success", "modified_count": result.modified_count})
        else:
            # return jsonify({"status": "failed", "modified_count": result.modified_count})
            return redirect("/billlist")
    bill_detail = list(collection.find({'_id':ObjectId(id)}))[0]
    context = {'bill_detail':bill_detail,'bill_number':bill_number()}
    return render_template('master/billedit.html',context=context)