import os
import csv
from collections import defaultdict

from flask import (Flask,
                   render_template,
                   jsonify)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('s0_graph', template_folder=tmpl_dir)
app.debug = True


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/read")
def get_reading():
    readings = defaultdict(list)
    timestamps = []
    with open("testdata.csv") as csv_file:
        csvreader = csv.reader(csv_file, delimiter=';')
        for row in csvreader:
            timestamps.append(row[1])
            for index,col in enumerate(row[2:]):
                readings["sensor_%d" % index].append(float(col))
    return jsonify(dict(series=[dict(name=key,data=value)
                                for key,value in readings.items()],
                        categories=timestamps))



if __name__ == "__main__":
    app.run()
