from flask import Flask, render_template # for Flask app
# from datetime import datetime  # for date and time formatting
import datetime
import pyproj # for coordinates transformation
from pymongo import MongoClient
import dns

# instantiation of Flask class
app = Flask(__name__)

## MongoDB Atlas M0 cluster
# client = MongoClient("mongodb+srv://wyao:yao14@citation-bapzv.mongodb.net/test?retryWrites=true&w=majority")
# db = client.citation

## MongoDB Atlas M10 cluster
# client = MongoClient("mongodb+srv://wyao:yao14@cluster0-ubllg.mongodb.net/test?retryWrites=true&w=majority")
# db = client.citation

## MongoDB local
# client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
# client = MongoClient("mongodb://db:27017")
client = MongoClient("mongodb://localhost:27017")
db = client.citation2

# Home page
@app.route('/')
def home_page():
    return render_template('index_bootstrap.html')

# Sub page to show citation count vs issue date
@app.route('/date')
def date():

    # get a range of dates
    startDate = datetime.date(2018,1,1)
    Ndays = 365
    allDate = [str(startDate + datetime.timedelta(days = x)) for x in range(Ndays)]

    # get the total citation count for each issue date
    citationCountByDate = [db.record2.find({"Issue Date": allDate[y] + "T00:00:00.000"},{"Issue Date": 1, '_id': 0}).count() for y in range(Ndays)]

    # line chart with pan and zoom-in features
    return render_template('zoom_date.html', labels=allDate, values=citationCountByDate)

# sub page to show citation count for each month of a year
@app.route('/month')
def countCitationByMonth():

    # string components to concatenate into date strings
    year = ['2016-','2017-','2018-','2019-']
    mmDiv_low = ['01-01','02-01','03-01','04-01','05-01','06-01','07-01','08-01','09-01','10-01','11-01','12-01']
    mmDiv_high = ['01-31','02-28','03-31','04-30','05-31','06-30','07-31','08-31','09-30','10-31','11-30','12-31']
    decorator = 'T00:00:00.000'
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']

    citationCountByMonth = []
    # count citations for each month of the selected year
    for yy in year:
        for mm in range(12):
            monthCount = db.record2.find(
            {"Issue Date": {"$gte": yy + mmDiv_low[mm] + decorator, "$lte":yy + mmDiv_high[mm] + decorator}}).count()
            citationCountByMonth.append(monthCount)

    # line chart with multiple lines
    return render_template('line_month.html', labels=month, values1=citationCountByMonth[0:12], values2=citationCountByMonth[12:24], values3=citationCountByMonth[24:36], values4=citationCountByMonth[36:43])

# Sub page to show citation count vs day of week
@app.route('/day')
def countCitationByDay():
    # get a range of dates
    startDate = datetime.date(2018,1,1)
    Ndays = 365
    allDate = [str(startDate + datetime.timedelta(days = x)) for x in range(Ndays)]

    # initialization of the lists for citation count and corresponding day
    citationCountByDay = [0]*7
    week = ['Mon', 'Tue', 'Wed',
            'Thu', 'Fri', 'Sat', 'Sun']

    for date in allDate:
        # get citation count for each date
        dateCount = db.record2.find(
            {"Issue Date": date + "T00:00:00.000"}, {"Issue Date": 1, '_id': 0}).count()
        # convert date in YYYY-MM-DD format to day of week (format: 'Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday')
        day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%a')
        # get total citation number for each day of week
        citationCountByDay[week.index(day)] += dateCount

    # convert citation count to percentage
    citationPercentByDay = [x / sum(citationCountByDay) for x in citationCountByDay]
    citationPercentByDay = [round(i*100,1) for i in citationPercentByDay]

    # colors = [
    #     "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    #     "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    #     "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    # pie chart with labels
    return render_template('pie_day.html', labels=week, values=citationPercentByDay)


# Sub page to show citation count vs issue time
@app.route('/time')
def countCitationsByTime():
    # set date range
    startDate = "2016-01-01T00:00:00.000"
    endDate = "2016-12-31T00:00:00.000"

    # histogram initialization
    hist = [0]*24
    bins = [0]*25

    # get citation count for each hour
    for i in range(24):
        hist[i] = db.record2.find({"Issue time": {"$gte":0+i*100, "$lt":100+i*100}, "Issue Date": {"$gte": startDate, "$lte":endDate}}).count()
        bins[i] = 0+i*100

    # for i in range(24):
    #     hist[i] = db.record2.find({"Issue time": {"$gte":0+i*100, "$lt":100+i*100}}).count()
    #     bins[i] = 0+i*100

    countSum = sum(hist)
    # convert citation count to percentage
    hist_pct = []
    for x in hist:
        hist_pct.append(x * 100 / countSum)

    binTime = []
    # change time format from hhmm to hh:mm
    for time in bins:
        binTime.append(datetime.datetime.strptime(str(time).zfill(4), '%H%M').strftime('%H')) #e.g. of zfill(4): 10-->0010, 131-->0131, 1351-->1351

    # histogram
    return render_template('hist_time.html',labels=binTime, values=hist_pct)

# Sub page to show citation count vs car make
@app.route('/make')
def countCitationsByMake():

    # set date range
    startDate = "2018-01-01T00:00:00.000"
    endDate = "2018-12-31T00:00:00.000"

    # get all car makes
    # allMake = db.record2.find({"Issue Date": {"$gte": startDate, "$lte":endDate}}).distinct("Make")
    allMake = db.record2.distinct("Make")

    citationCountByMake = []
    # get citation count for each car make in the defined date range
    for make in allMake:
        citationCountByMake.append(db.record2.find(
            {'Make': make, "Issue Date": {"$gte": startDate, "$lte":endDate}}).count())

    # set the number of car makes in parking citation to show
    limit = 15
    # sort the citation count by car make in a descending order
    sortedCountByMake = sorted(citationCountByMake, reverse=True)
    # get the index of the sorted list of citation counts
    index = sorted(range(len(citationCountByMake)),
                   key=citationCountByMake.__getitem__, reverse=True) #magic function
    sortedMake = []
    # sort car makes by the order of citation counts
    for n in range(limit):
        sortedMake.append(allMake[index[n]])

    # bar chart
    return render_template('bar_make.html', labels=sortedMake, values=sortedCountByMake[0:limit])

# # Sub page to show citation count vs car violation
# @app.route('/violation')
# def countCitationByViolation():
#     '''
#     When a $sort precedes a $limit and there are no intervening stages
#     that modify the number of documents, the optimizer can coalesce the $limit into the $sort.
#     This allows the $sort operation to only maintain the top n results as it progresses,
#     where n is the specified limit, and ensures that MongoDB only needs to store n items in memory.
#     '''
#     # sort violation types by the order of citation counts
#     topViolation = list(db.record2.aggregate(
#         [{"$sortByCount": "$Violation Description"}, {"$limit": 10}]))  # $limit sets the number of targets to be processed and displayed

#     labels = []
#     values = []

#     for violation in topViolation:
#         labels.append(violation['_id'])
#         values.append(violation['count'])
#     # bar chart
#     return render_template('bar_chart.html', title='Top violation types reported in LA parking citation', max=3000000, labels=labels, values=values)

# Sub page to citation count vs fine amount
@app.route('/fine')
def countCitationsByFine():

    bins = [0,50,100,350,550]
    hist = [0]*4

    # get citation count for each bin
    for i in range(len(hist)):
        hist[i] = db.record2.find({"Fine amount": {"$gte":bins[i], "$lt":bins[i+1]}}).count()

    # histogram
    return render_template('hist_fine.html', labels=bins, values=hist)

# sub page to show top citation locations
@app.route('/map')
def displayTopLocations():

    startDate = "2019-07-04T00:00:00.000"
    endDate = "2019-07-07T00:00:00.000"
    # get all citation locations, speed up DB query by limiting the date range
    allLocation = db.record2.find(
        {"Issue Date": {"$gte": startDate, "$lte":endDate}}).distinct("Location")
    # allLocation = db.record2.find(
    #     {"Issue Date": startDate}).distinct("Location")

    citationCountByLocation = []
    # get the total citation count for each location within the defined time period
    for location in allLocation:
        citationCountByLocation.append(db.record2.find(
            {"Location": location, "Issue Date": {"$gte": startDate, "$lte":endDate}}).count())
        # citationCountByLocation.append(db.record2.find(
        #     {"Location": location, "Issue Date": startDate}).count())

    limit = 10
    sortedCountByLocation = sorted(citationCountByLocation, reverse=True)
    # get the index of the sorted list of citation counts
    index = sorted(range(len(citationCountByLocation)),
                   key=citationCountByLocation.__getitem__, reverse=True) #magic function
    sortedLocation = []
    # sort locations by the order of citation counts
    for n in range(limit):
        sortedLocation.append(allLocation[index[n]])

    lat = []
    lng = []
    # get coordinates of the corresponding locations
    for loc in sortedLocation:
        # lat_temp1 = db.record2.find({"Location": loc, "Issue Date": startDate}).distinct("Latitude")
        lat_temp1 = db.record2.find({"Location": loc, "Issue Date": {"$gte": startDate, "$lte":endDate}}).distinct("Latitude")
        lat.append(lat_temp1[0])
        # lng_temp1 = db.record2.find({"Location": loc, "Issue Date": startDate}).distinct("Longitude")
        lng_temp1 = db.record2.find({"Location": loc, "Issue Date": {"$gte": startDate, "$lte":endDate}}).distinct("Longitude")
        lng.append(lng_temp1[0])

    # coordinate conversion
    pm = '+proj=lcc +lat_1=34.03333333333333 +lat_2=35.46666666666667 +lat_0=33.5 +lon_0=-118 +x_0=2000000 +y_0=500000.0000000002 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs'
    for itr in range(len(lat)):
        lng[itr],lat[itr] = pyproj.transform(pyproj.Proj(pm,preserve_units = True), pyproj.Proj("+init=epsg:4326"), lat[itr],lng[itr])

    # google maps with markers
    return render_template('gmap_bootstrap.html',lat=lat, lng=lng, loc=sortedLocation, count=sortedCountByLocation[0:limit])


# activate debug mode; only true when running directly from Python
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
