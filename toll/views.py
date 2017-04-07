from django.shortcuts import render
import requests
from django.http import HttpResponse
import json,uuid
from toll.models import users,vehicles,toll
from Tkinter import *
import thread
from twilio.rest import TwilioRestClient

account_sid = "AC587b3320c8851a77cf101709374c276a" # Your Account SID from www.twilio.com/console
auth_token  = "c68286d5124fef9f0a548036105ab08a"  # Your Auth Token from www.twilio.com/console


# Create your views here.

def getaccesstoken(request):
    resp=requests.post('https://api.instamojo.com/oauth2/token/', data={
      'grant_type': 'client_credentials',
      'client_id': 'OgY5fow2DVy15Vo3HDWaMEcrYTSEs4okZlYqFrJN',
      'client_secret': 'jmJSZGUL3ySOFFuWmYrIs46N157HNJVEg54YPFPu2an6khwUNmxKVBOVnHXT16McHckdd0c2qTXj2FhOzr4pombWCTY85KI4J8OJrRPuENRi5wrtP1NTpizH1p4Q7VZq'
})
#    data=resp.data
#    data=json.loads(data)
    data= resp.content
    data=json.loads(data)
    access_token= data['access_token']
    transaction_id = str(uuid.uuid4())
    print access_token
    print transaction_id
    response_data={}
    response_data['access_token']=access_token
    response_data['transaction_id']=transaction_id
    return HttpResponse(json.dumps(response_data),content_type="application/json")


def demo(request):
    data=request.GET.get('q');
    print data
    return HttpResponse('q')


def authenticate(request):
    data=json.loads(request.body)
    user_id=data['user_id']
    password=data['password']
    resp={}

    try:
        u=users.objects.get(pk=user_id)
        if u.password==password:
            resp['status']='valid'
            resp['name']=u.Name
            resp['mobile']=u.Mobile
            resp['email']=u.email
            resp['user_id']=u.user_id
            resp['balance']=u.rto_balance
            listdata=u.getvehicles()
            n=len(listdata)
            resp['count']=n
            print n
            resp['vehicles']=listdata
        else:
            resp['status']='invalid'
    except users.DoesNotExist:
        resp['status']='error'
    return HttpResponse(json.dumps(resp),content_type="application/json")

def check_recharge(request):
    data=json.loads(request.body)
    transaction_id=data['transaction_id']
    amount=data['amount']
    payment_id=str(uuid.uuid4())
    headers={'X-Api-Key':'5cf6635cd7ce33abf5d3b15d6c05a9b1','X-Auth-Token':'8b92c7a67f447b3214f15831eadd2270'}
    resp=requests.post('https://www.instamojo.com/api/1.1/payment-requests/',data={
    'id':payment_id,
    'payment_id':transaction_id
    },headers=headers)
    return "hej"

#    data=resp.content
#    return data
'''    data=json.loads(data)
    payment=data['payment']
    status=payment['status']
    response={}
    if status=='Credit':
        amt=payment['amount']
        if amt==amount:
            response['status']='valid'
        else:
            response['status']='error'
    else:
        response['status']='error'
    return HttpResponse(json.dumps(response),content_type="application/json")
'''


def validate_user(request):
    data=request.GET.get('q');
    print data
    rfid_value=data
    #rfid_value=data['value']
    toll_id=rfid_value[:3]
    vehicle_no=rfid_value[11:13]
    user_id=rfid_value[13]
    vehicle_type=rfid_value[14]
    print toll_id
    print user_id
    print vehicle_no
    print vehicle_type
    resp='a'
    try:
        v=vehicles.objects.get(pk=vehicle_no)
        print v.vehicle_type
        type(v.vehicle_type)
        print "hfjd"
        type(vehicle_type)
        if int(v.vehicle_type)==int(vehicle_type):
            if v.user_id.user_id==user_id:
                amt=amount_to_deduct(toll_id,vehicle_type)
                if(check_balance(user_id,amt)):
                    print "all valid"
                    #send_msg()
                    #thread.start_new_thread(open_gate,())
                    resp='q'     #yes
                 #carry_out payment in new thread
                else:
                    print "insufficient funds"
                    resp='z'       #insufficient funds
            else:
                print "wrong user id"
                resp='z'      #no
        else:
            print "mismatch vehicle type"
            resp='z'          #no
    except vehicles.DoesNotExist:
        print "vehicles does not exist"
        resp='z'
		#resp='z'              #no
    print resp
    return HttpResponse(resp)


def amount_to_deduct(toll_id,vehicle_type):
    try:
        t=toll.objects.get(pk=toll_id)
        if vehicle_type==2:
            return t.car_price
        elif vehicle_type==4:
            return t.bike_price
        elif vehicle_type==6:
            return t.bus_price
        else:
			return t.truck_price
    except toll.DoesNotExist:
        return 'error'





#rfid deduction
def check_balance(user_id,amt):
    u=users.objects.get(pk=user_id)
    if u.rto_balance<amt:
        return False
    u.deduct_amt(amt)
    return True


#app recharge
def update_bal(request):
    data=json.loads(request.body)
    print data
    user_id=data['user_id']
    amt=data['addbalance']
    resp={}
    try:
        u=users.objects.get(pk=user_id)
        u.add_amt(amt)
        resp['status']='ok'
    except users.DoesNotExist:
        resp['status']='not ok'
    return HttpResponse(json.dumps(resp),content_type="application/json")





def get_toll_details(request):
    listdata=[]
    n=len(toll.objects.all())
    for i in range(0,n):
        tolld={}
        t=toll.objects.all()[i]
        tolld['id']=t.toll_id
        tolld['name']=t.toll_name
        tolld['state']=t.state
        tolld['latitude']=t.latitude
        tolld['longitude']=t.longitude
        tolld['services']=t.services
        tolld['car']=t.car_price
        tolld['bike']=t.bike_price
        tolld['bus']=t.bus_price
        tolld['truck']=t.truck_price
        listdata.append(tolld)
    data={}
    data['count']=n
    data['toll_data']=listdata
    return HttpResponse(json.dumps(data),content_type="application/json")




def get_new_balance(request):
    data=json.loads(request.body)
    user_id=data['user_id']
    u=users.objects.get(pk=user_id)
    resp={}
    resp['balance']=u.rto_balance
    return HttpResponse(json.dumps(resp),content_type="application/json")

def open_gate():
    master = Tk()
    status="Open Gate"
    msg = Message(master, text = status)
    msg.config(bg='lightgreen', font=('times', 50, 'italic'))
    msg.place(height=200,width=500,x=400,y=200)
    master.after(5000, lambda: master.destroy())
    master.mainloop()


def send_msg():
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Payment done successfully",
    to="+918452078307",    # Replace with your phone number
    from_="+16463743039 ") # Replace with your Twilio number

    print(message.sid)
