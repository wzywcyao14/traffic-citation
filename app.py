from flask import Flask, render_template
# manges MongoDB connections for the Flask app.
from flask_pymongo import PyMongo

app = Flask(__name__)

# configuration handling
app.config['MONGO_URI'] = "mongodb://localhost:27017/citation"

mongo = PyMongo(app)


@app.route('/')
def home_page():
    # return "<h1>Welcome to the LA traffic citation analytics website!<h1>"
    return render_template('home.html')


@app.route('/make')
def make():
    '''
    When a $sort precedes a $limit and there are no intervening stages
    that modify the number of documents, the optimizer can coalesce the $limit into the $sort.
    This allows the $sort operation to only maintain the top n results as it progresses,
    where n is the specified limit, and ensures that MongoDB only needs to store n items in memory.
    '''
    topMake = list(mongo.db.record.aggregate(
        [{"$sortByCount": "$Make"}, {"$limit": 20}]))  # $limit sets the number of makes to be processed and displayed

    labels = []
    values = []
    for i in topMake:
        labels.append(i['_id'])
        values.append(i['count'])
    return render_template('bar_chart.html', title='Top car makes reported in LA parking citation', max=1800000, labels=labels, values=values)


@app.route('/violation')
def violation():

    topViolation = list(mongo.db.record.aggregate(
        [{"$sortByCount": "$Violation Description"}, {"$limit": 10}]))  # $limit sets the number of targets to be processed and displayed

    labels = []
    values = []
    for i in topViolation:
        labels.append(i['_id'])
        values.append(i['count'])
    return render_template('bar_chart.html', title='Top violation types reported in LA parking citation', max=3000000, labels=labels, values=values)


# @app.before_request
# def before_request():
#     g.start = time.time()


# @app.after_request
# def after_request(response):
#     diff = time.time() - g.start
#     if ((response.response) and
#         (200 <= response.status_code < 300) and
#             (response.content_type.startswith('text/html'))):
#         response.set_data(response.get_data().replace(
#             b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
#     return response


if __name__ == '__main__':
    app.run(debug=True)
