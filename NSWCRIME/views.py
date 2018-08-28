from flask import request, Flask, url_for, make_response, jsonify
from models import Area, Offense
from flask_restful import reqparse
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from auth import SECRET_KEY, login_required
from mongoengine import connect
import requests
import datetime
import xlrd
import pymongo
from collections import defaultdict
from werkzeug.contrib.atom import AtomFeed, FeedEntry
from dict2xml import dict2xml as xmlify
import json


app = Flask(__name__)

#dict initialization for postcode searching
postdic = defaultdict(list)
dict_url = 'AustralianLGApostcodemappings.xlsx'
data_url = xlrd.open_workbook(dict_url).sheets()[0]
for r in range(1, 1781):
    region = str(data_url.cell(r, 1).value).lower().replace(' ', '')
    postcode1 = int(data_url.cell(r, 2).value) #postcode -- int
    postdic[region].append(postcode1)


#Creating a data entry - admin only
@app.route('/areas', methods = ["POST"])
@login_required
def add_entry():
    connect(host='mongodb://yuyoux:yongbao1110@ds255539.mlab.com:55539/9321test')
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='LGA name input error')
    parser.add_argument('postcode', type=int, help='Postcode input error')
    args = parser.parse_args()
    postcode = args.get("postcode")#check postcode to find the LGA name
    ############################# postcode ######################################
    if postcode:
        name_list = []
        for k, v in postdic.items():
            for s in v:
                if s == postcode:
                    name_list.append(k) #regions founded

        if name_list == []: #check whether the input postcode in the postdic
            return jsonify(Input_postcode=False),404

        feed = AtomFeed(title='Multi-collections POST complete', feed_url=request.url)
        for a in Area.objects:
            for n in name_list:
                if a.name.lower().replace(' ', '') == n.lower().replace(' ', ''):
                    name_list.remove(n)
        for n in name_list:
            name = n
            url = 'http://127.0.0.1:5000' + url_for('show_entry', name=name)

            # download from the internet -- check 400 - if 2 not in 1 -- not up-to-date
            dld_url = 'http://www.bocsar.nsw.gov.au/Documents/RCS-Annual/'+name+'lga.xlsx'
            r = requests.get(dld_url)
            with open(name + 'lga.xlsx','wb') as f:
                f.write(r.content)

            excel_url = name + 'lga.xlsx'
            data = xlrd.open_workbook(excel_url).sheets()[0]
            id = 0  # initialisation id for embeded document
            p = []  # used to collect Offense()
            for row in range(7, 69):  # for further update
                id = id + 1
                offence_group = str(data.cell(row, 0).value)
                if offence_group != '':
                    backup = offence_group
                if offence_group == '':
                    offence_group = backup
                offence_type = str(data.cell(row, 1).value)
                incidents_2012 = str(data.cell(row, 2).value)
                rate_2012 = str(data.cell(row, 3).value)
                incidents_2013 = str(data.cell(row, 4).value)
                rate_2013 = str(data.cell(row, 5).value)
                incidents_2014 = str(data.cell(row, 6).value)
                rate_2014 = str(data.cell(row, 7).value)
                incidents_2015 = str(data.cell(row, 8).value)
                rate_2015 = str(data.cell(row, 9).value)
                incidents_2016 = str(data.cell(row, 10).value)
                rate_2016 = str(data.cell(row, 11).value)
                trend_24m = str(data.cell(row, 12).value)
                trend_60m = str(data.cell(row, 13).value)
                lga_rank = str(data.cell(row, 14).value)
                p.append(Offense(id, offence_group, offence_type, incidents_2012, rate_2012, incidents_2013, rate_2013, \
                                 incidents_2014, rate_2014, incidents_2015, rate_2015, incidents_2016, \
                                 rate_2016, trend_24m, trend_60m, lga_rank))
            t = Area(name, p)
            t.save()
            entry = FeedEntry(title=name, url=url, updated=datetime.datetime.utcnow(), author={'name': 'admin'})
            feed.add(entry)

        response = make_response(feed.to_string())
        response.mimetype = "application/atom+xml"

    ############################# name ######################################
    else: #if postcode not given, check the name field
        name = args.get("name").lower().replace(' ', '')
        if not name:
            return jsonify(Input=False), 404
        url = 'http://127.0.0.1:5000' + url_for('show_entry', name=name)

        #if LGA or postcode that already has been imported before
        for a in Area.objects:
            if a.name.lower().replace(' ', '') == name.lower().replace(' ', ''):
                feed = AtomFeed(title='Already existed', feed_url=url)
                entry = FeedEntry(title=name, url=url, updated=datetime.datetime.utcnow(),
                                author={'name': 'admin'})
                feed.add(entry)
                response = make_response(feed.to_string())
                response.mimetype = "application/atom+xml"
                return response, 200

        #download from the internet -- check 400 - if 2 not in 1 -- not up-to-date
        dld_url = 'http://www.bocsar.nsw.gov.au/Documents/RCS-Annual/'+name+'lga.xlsx'
        r = requests.get(dld_url)
        with open(name + 'lga.xlsx','wb') as f:
           f.write(r.content)

        excel_url = name + 'lga.xlsx'
        data = xlrd.open_workbook(excel_url).sheets()[0]
        id = 0 #initialisation id for embeded document
        p = [] #used to collect Offense()
        for row in range(7, 69): #for further update
            id = id+1
            offence_group = str(data.cell(row, 0).value)
            if offence_group != '':
                backup = offence_group
            if offence_group == '':
                offence_group = backup
            offence_type = str(data.cell(row, 1).value)
            incidents_2012 = str(data.cell(row, 2).value)
            rate_2012 = str(data.cell(row, 3).value)
            incidents_2013 = str(data.cell(row, 4).value)
            rate_2013 = str(data.cell(row, 5).value)
            incidents_2014 = str(data.cell(row, 6).value)
            rate_2014 = str(data.cell(row, 7).value)
            incidents_2015 = str(data.cell(row, 8).value)
            rate_2015 = str(data.cell(row, 9).value)
            incidents_2016 = str(data.cell(row, 10).value)
            rate_2016 = str(data.cell(row, 11).value)
            trend_24m = str(data.cell(row, 12).value)
            trend_60m = str(data.cell(row, 13).value)
            lga_rank = str(data.cell(row, 14).value)
            p.append(Offense(id, offence_group, offence_type, incidents_2012, rate_2012, incidents_2013, rate_2013, \
                            incidents_2014, rate_2014, incidents_2015, rate_2015, incidents_2016, \
                            rate_2016, trend_24m, trend_60m, lga_rank))
        t = Area(name,p)
        t.save()

        feed = AtomFeed(title='Sucess POST Activity', feed_url=url)
        entry = FeedEntry(title=name, url=url, updated=datetime.datetime.utcnow(), author={'name': 'admin'})
        feed.add(entry)
        response = make_response(feed.to_string())
        response.mimetype = "application/atom+xml"

    return response, 201


#Deleting a data entry - admin only
@app.route('/areas/<name>', methods = ["DELETE"])
@login_required
def delete_entry(name):
    connect(host='mongodb://yuyoux:yongbao1110@ds255539.mlab.com:55539/9321test')
    for a in Area.objects:
        if a.name.lower().replace(' ', '') == name.lower().replace(' ', ''):
            Area.objects(name = name.lower().replace(' ', '')).delete()
            return jsonify(LGA_name=True), 200
    return jsonify(LGA_name=False), 404


#Retreiving the available collection - admin and guest access
@app.route('/areas', methods = ["GET"])
def show_collection():
    connect(host='mongodb://yuyoux:yongbao1110@ds255539.mlab.com:55539/9321test')
    feed = AtomFeed(title='All Available Collections',feed_url=request.url)
    for a in Area.objects:
        data = json.loads(a.to_json())
        data2 = xmlify(data, wrap="all", indent="  ")
        url = 'http://127.0.0.1:5000'+ url_for('show_entry', name=a.name)
        entry = FeedEntry(title=a.name, url=url, updated=datetime.datetime.utcnow(), author={'name': 'admin'}, \
                      content_type="application/xml",content= data2)
        feed.add(entry)
    response = make_response(feed.to_string())
    response.mimetype = "application/atom+xml"
    return response, 200


#Retreiving a data entry - admin and guest access
@app.route('/areas/<name>', methods = ["GET"])
def show_entry(name):
    connect(host='mongodb://yuyoux:yongbao1110@ds255539.mlab.com:55539/9321test')
    feed = AtomFeed(title='Single Collection', feed_url=request.url)
    for a in Area.objects:
        if a.name.lower().replace(' ', '') == name.lower().replace(' ', ''):
            #print(xmlify(a.offenses,wrap="all", indent="  "))
            data = json.loads(a.to_json())
            data2 = xmlify(data, wrap="all", indent="  ")
            entry = FeedEntry(title = a.name, url=request.url, updated=datetime.datetime.utcnow(),author = {'name':'admin'}, \
                              content_type="application/xml",content = data2)
            feed.add(entry)
            response = make_response(feed.to_string())
            response.mimetype = "application/atom+xml"
            return response, 200 #ATOM
    return jsonify(LGA_name=False), 404


#Retreiving data entries with filter - admin and guest access
@app.route('/areas/filter', methods = ["GET"])
def filter_entry():
    connect(host='mongodb://yuyoux:yongbao1110@ds255539.mlab.com:55539/9321test')
    raw_str = str(request.url)
    raw_str2 = raw_str.split('+')

    if raw_str2[4] == 'lgaName': #query-type-one
        name1 = raw_str2[2]
        name2 = raw_str2[6]
        feed = AtomFeed(title='Query 1 Search Results', feed_url=request.url)
        url1 = 'http://127.0.0.1:5000' + url_for('show_entry', name=name1)
        url2 = 'http://127.0.0.1:5000' + url_for('show_entry', name=name2)
        for a in Area.objects: #Search for name 1
            if a.name.lower().replace(' ', '') == name1.lower().replace(' ', ''):
                data = json.loads(a.to_json())
                data2 = xmlify(data, wrap="all", indent="  ")
                entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                           author={'name': 'admin'}, \
                          content_type="application/xml", content=data2)
                feed.add(entry)
        for a in Area.objects: #Search for name 2
            if a.name.lower().replace(' ', '') == name2.lower().replace(' ', ''):
                data = json.loads(a.to_json())
                data2 = xmlify(data, wrap="all", indent="  ")
                entry = FeedEntry(title=a.name, url=url2, updated=datetime.datetime.utcnow(),
                           author={'name': 'admin'}, \
                          content_type="application/xml", content=data2)
                feed.add(entry)
        response = make_response(feed.to_string())
        response.mimetype = "application/atom+xml"
        return response, 200

    elif raw_str2[4] == 'year': #query-type-two
        name1 = raw_str2[2]
        year1 = raw_str2[6]
        feed = AtomFeed(title='Query 2 Search Results', feed_url=request.url)
        url1 = 'http://127.0.0.1:5000' + url_for('show_entry', name=name1)

        for a in Area.objects: #Search for name
            if a.name.lower().replace(' ', '') == name1.lower().replace(' ', ''):
                if year1 == '2014':
                    fakedb = defaultdict(list)
                    for stas in a.offenses:
                        fakedb[stas.id].append({'offence_group':stas.offence_group, 'offence_type':stas.offence_type, \
                                                            'incidents_2014':stas.incidents_2014, 'rate_2014':stas.rate_2014})
                    j_fakedb = json.dumps(fakedb,indent=4)
                    data2 = xmlify(j_fakedb, wrap="all", indent="  ")
                    entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                                     author={'name': 'admin'}, \
                                     content_type="application/xml", content=data2)
                    feed.add(entry)
                    response = make_response(feed.to_string())
                    response.mimetype = "application/atom+xml"
                    return response, 200
                elif year1 == '2015':
                    fakedb = defaultdict(list)
                    for stas in a.offenses:
                        fakedb[stas.id].append({'offence_group': stas.offence_group, 'offence_type': stas.offence_type, \
                                                'incidents_2015': stas.incidents_2015, 'rate_2015': stas.rate_2015})
                    j_fakedb = json.dumps(fakedb, indent=4)
                    data2 = xmlify(j_fakedb, wrap="all", indent="  ")
                    entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                                      author={'name': 'admin'}, \
                                      content_type="application/xml", content=data2)
                    feed.add(entry)
                    response = make_response(feed.to_string())
                    response.mimetype = "application/atom+xml"
                    return response, 200
                elif year1 == '2016':
                    fakedb = defaultdict(list)
                    for stas in a.offenses:
                        fakedb[stas.id].append({'offence_group': stas.offence_group, 'offence_type': stas.offence_type, \
                                                'incidents_2016': stas.incidents_2016, 'rate_2016': stas.rate_2016})
                    j_fakedb = json.dumps(fakedb, indent=4)
                    data2 = xmlify(j_fakedb, wrap="all", indent="  ")
                    entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                                      author={'name': 'admin'}, \
                                      content_type="application/xml", content=data2)
                    feed.add(entry)
                    response = make_response(feed.to_string())
                    response.mimetype = "application/atom+xml"
                    return response, 200
                elif year1 == '2012':
                    fakedb = defaultdict(list)
                    for stas in a.offenses:
                        fakedb[stas.id].append({'offence_group': stas.offence_group, 'offence_type': stas.offence_type, \
                                                'incidents_2012': stas.incidents_2012, 'rate_2012': stas.rate_2012})
                    j_fakedb = json.dumps(fakedb, indent=4)
                    data2 = xmlify(j_fakedb, wrap="all", indent="  ")
                    entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                                      author={'name': 'admin'}, \
                                      content_type="application/xml", content=data2)
                    feed.add(entry)
                    response = make_response(feed.to_string())
                    response.mimetype = "application/atom+xml"
                    return response, 200
                elif year1 == '2013':
                    fakedb = defaultdict(list)
                    for stas in a.offenses:
                        fakedb[stas.id].append({'offence_group': stas.offence_group, 'offence_type': stas.offence_type, \
                                                'incidents_2013': stas.incidents_2013, 'rate_2013': stas.rate_2013})
                    j_fakedb = json.dumps(fakedb, indent=4)
                    data2 = xmlify(j_fakedb, wrap="all", indent="  ")
                    entry = FeedEntry(title=a.name, url=url1, updated=datetime.datetime.utcnow(),
                                      author={'name': 'admin'}, \
                                      content_type="application/xml", content=data2)
                    feed.add(entry)
                    response = make_response(feed.to_string())
                    response.mimetype = "application/atom+xml"
                    return response, 200
                else:
                    return jsonify(Input_Year=False), 400

    return jsonify(Input=False),404



#Token processing
@app.route("/auth", methods = ["GET"])
def generate_token():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    username = args.get("username")
    password = args.get("password")

    s = Serializer(SECRET_KEY, expires_in=600)
    token = s.dumps(username)
    if username == 'admin' and password == 'admin':
        return token.decode()
    return 404

if __name__ == '__main__':
    app.run()
