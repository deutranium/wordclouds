from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pandas_implementation import *
from df_text import *

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		Data_extracted = get_DataFrame(f)
		start_date = Data_extracted['Date'].iloc[0]
		end_date = Data_extracted['Date'].iloc[-1]
		df_to_text(Data_extracted)
		return render_template('uploader.html', start_date=start_date, end_date=end_date)

if __name__ == '__main__':
	app.run(debug=True)
