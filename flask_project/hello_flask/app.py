from flask import Flask, request
from flask import json,jsonify
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


app = Flask(__name__)

@app.route('/getAnyHotelDetails', methods=['GET', 'POST'])
def getAnyHotelDetails():
	hotel_location = request.args.get('hotel_location').split(',')[0]
	checkin_date = request.args.get('checkin_date')
	checkout_date = request.args.get('checkout_date')
	room_no = request.args.get('room_no')

	response = requests.get("http://localhost:9200/hotels/hotel/hotel_list")
	str_response = json.loads(response.text)
	hotel_list = str_response["_source"]["data"]

	success = True
	hotel = hotel_list[0]
	hotel_name = hotel["hotel_name"]
	price = hotel["bookings_price"][0]


	'''
	for hotel in hotel_list:
		if not hotel["city"] == hotel_location:
			continue;
		if not hotel["checkin_date"] == checkin_date:
			continue;
		if not checkout_date in hotel["checkout_date"]:
			continue;

		index = hotel["checkout_date"].index("bar")
		if hotel["no_of_rooms"][index] == room_no:
			hotel_name = hotel["hotel_name"]
			price = hotel["bookings_price"][index]
			success = True
			break;
	'''
	if success:
		return hotel_name + "\n" + price
	else:
		return hotel_location + "\n" + checkin_date + "\n" + checkout_date + "\n" + room_no

	#print str_response["_source"]["locations"]["bangalore"]["rooms"]["standard room, 1 double bed"]
	#print ss
	#


@app.route('/getHotelRoomDetails', methods=['GET', 'POST'])
def getHotelRoomDetails():
	hotel_name = request.args.get('hotel_name')
	hotel_location = request.args.get('hotel_location')
	checkin_date = request.args.get('checkin_date')
	datetimeobject = datetime.strptime(checkin_date,'%d/%m/%Y')
	checkin_date = datetimeobject.strftime('%Y-%m-%d')
	checkout_date = request.args.get('checkout_date')
	datetimeobject = datetime.strptime(checkout_date,'%d/%m/%Y')
	checkout_date = datetimeobject.strftime('%Y-%m-%d')
	room_no = request.args.get('room_no')
	success = False

	#print hotel_name + "\n" + hotel_location + "\n" + checkin_date + "\n" + checkout_date + "\n" + room_no
	response = requests.get("http://localhost:9200/hotels/hotel/hotel_list")
	str_response = json.loads(response.text)

	hotel_list = str_response["_source"]["data"]



	count = 0
	for hotel in hotel_list:
		count+=1
		#print count
		if not hotel["hotel_name"].strip(".") == hotel_name:
			#print "Match not found for hotel name ", hotel_name, "  !=  ",  hotel["hotel_name"]
			continue;
		if not hotel["city"] == hotel_location:
			#print "Match not found for hotel location ", hotel_location, "  !=  ",  hotel["city"]
			continue;
		if not hotel["checkin_date"] == checkin_date:
			#print "Match not found for hotel name ", checkin_date, "  !=  ",  hotel["checkin_date"]
			continue;
		if not checkout_date in hotel["checkout_date"]:
			#print "Match not found for checkout date"
			continue;

		index = 0
		#print "Match found going inside for loop"
		json_response = {}
		json_response["room_type"] = []
		json_response["booking_price"] = []
		json_response["expedia_price"] = []

		for checkout in hotel["checkout_date"]:
			#print
			#print checkout == checkout_date
			#print hotel["sold_out_flag"][index] == "0"
			#print hotel["no_of_rooms"][index] == room_no
			#print
			if checkout == checkout_date and hotel["sold_out_flag"][index] == "0" and hotel["no_of_rooms"][index] == room_no:
				#print "Match found"
				booking_price = hotel["bookings_price"][index]
				expedia_price = hotel["expedia_price"][index]
				room_type = hotel["room_name"][index]
				json_response["room_type"].append(room_type)
				json_response["booking_price"].append(booking_price)
				json_response["expedia_price"].append(expedia_price)
				#print "return rooms with  room name = ", room_type , " booking price ", booking_price , " expedia_price  ",expedia_price
			index+=1


	print json_response
	return jsonify(json_response)

if __name__ == '__main__':
	app.run(debug=True)
