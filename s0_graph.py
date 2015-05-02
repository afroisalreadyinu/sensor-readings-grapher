import os
import csv
import glob
from collections import defaultdict
from datetime import datetime
from StringIO import StringIO
from contextlib import closing

from flask import (Flask,
                   render_template,
                   jsonify)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('s0_graph', template_folder=tmpl_dir)
app.debug = True

DATA_DIR = os.environ['DATA_DIR']
FILE_FORMAT = "%Y-%m-%d.csv"
LAST_POINTS_COUNT = 50

def compare_filenames(f1, f2):
    _, f1 = os.path.split(f1)
    _, f2 = os.path.split(f2)
    if datetime.strptime(f1, FILE_FORMAT) > datetime.strptime(f2, FILE_FORMAT):
        return 1
    return -1

def concat_oldest_files(base_dir):
    csvs = glob.glob(os.path.join(base_dir, "*.csv"))
    files = sorted(csvs, cmp=compare_filenames, reverse=True)[:2]
    data = []
    for _file in reversed(files):
        with open(_file, 'r') as data_file:
            data.extend(data_file.readlines())
    return "".join(data[:LAST_POINTS_COUNT]).strip()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/read")
def get_reading():
    data = concat_oldest_files(DATA_DIR)
    readings = defaultdict(list)
    timestamps = []
    with closing(StringIO(data)) as csv_file:
        csvreader = csv.reader(csv_file, delimiter=';')
        for row in csvreader:
            timestamps.append(row[0])
            for index,col in enumerate(row[1:]):
                readings["sensor_%d" % index].append(float(col))
    return jsonify(dict(series=[dict(name=key,data=value)
                                for key,value in readings.items()],
                        categories=timestamps))


if __name__ == "__main__":
    app.run()
