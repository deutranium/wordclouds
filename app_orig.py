from flask import Flask, render_template, request
from PySripts.pandas_implementation import *
from PySripts.df_text import *
from PySripts.wordcloud_generator import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/', methods = ['POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		decoded = f.read().decode('utf-8')
		Data_extracted = get_DataFrame(decoded)
		start_date = request.form.get("start_date")
		end_date = request.form.get("end_date")
		print(end_date)
		print(start_date)


		if (start_date!='') & (end_date!=''):
			start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
			end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
			if (start_date>end_date):
				return render_template('index.html', date_error=1)
			Data_extracted = Data_extracted[ (Data_extracted.Date>=start_date) & (Data_extracted.Date<=end_date) ]

		elif (start_date!=''):
			start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
			print(start_date)
			Data_extracted = Data_extracted[ (Data_extracted.Date>=start_date) ]

		elif (end_date!=''):
			end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
			Data_extracted = Data_extracted[ Data_extracted.Date<=end_date ]


		if(len(Data_extracted)==0):
			return render_template("index.html", no_element_error=1)
		
		txt = df_to_text(Data_extracted)
		wc_created = create_wc(txt)
		return render_template('index.html', plot=1, url ='/static/WordCloud.png')

@app.after_request
def add_header(response):
	"""
		Add headers to both force latest IE rendering engine or Chrome Frame,
		and also to cache the rendered page for 10 minutes.
		"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response


if __name__ == '__main__':
	app.run(debug=True)