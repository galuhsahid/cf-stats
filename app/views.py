from flask import render_template, flash, redirect, request
from app import app
from .forms import SubmitForm
from werkzeug import secure_filename
import StringIO
import base64
import pandas as pd
import matplotlib 
matplotlib.use('Agg') # PNG plotting 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

@app.route('/')
@app.route('/index')
def index():
    form = SubmitForm()
    if request.method == 'POST' and form.validate_on_submit():
    	title = form.title.data
    	theFile = secure_filename(form.myFile.data.filename)
    	form.myFile.data.save('uploads/'+myFile)
        return redirect(url_for('result'))
    return render_template('index.html', form=form)

@app.route('/result', methods=['GET', 'POST'])
def result():
	form = SubmitForm()

	# Import csv
	df = pd.read_csv(form.myFile.data)

	# Convert registered_at from object to datetime
	df['registered_at'] = pd.to_datetime(df['registered_at'])

	# Begin plotting
	df["count"] = 1
	df['registered_at_date'] = pd.DatetimeIndex(df.registered_at).normalize()
	results = df.set_index('registered_at_date')
	running_results = results.groupby(pd.TimeGrouper('D'))["count"].count().cumsum()
	
	img = StringIO.StringIO()

	step = pd.Series(range(0,len(running_results)), name="# of days")
	sns.plt.title(form.title.data)
	sns.tsplot(running_results, value="Registrants", time=step, color="husl")

	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue())

	total = df.shape[0]

	# Begin calculation
	today = datetime.date.today()
	registration_open = form.registration_opens.data
	registration_close = form.registration_closes.data
	diff = registration_close - today
	diff_days = diff.days

	# Create pivot table to see day-to-day details
	date_pivot_table = df[['registered_at_date', 'count']].groupby(['registered_at_date']).agg(['count'])
	total = (date_pivot_table.shape[0])+1
	days_until_today_dt = today - registration_open
	days_until_today = days_until_today_dt.days
	rate = total/days_until_today

	target = form.target.data
	diff_target = target - total

	target_rate = diff_target/diff.days

	return render_template('result.html', title='Sup yo', form=form, plot_url=plot_url, total=total, rate=rate, diff_target=diff_target, target_rate=target_rate, diff_days=diff_days)