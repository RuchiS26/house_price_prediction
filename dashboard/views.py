from django.shortcuts import render,redirect
from .models import DataStore
from .forms import DataForm

import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt

def dashboard_setup(request):
	
	avail_data = DataStore.objects.all().order_by('date_added')

	if request.method == 'POST':
		dataform = DataForm(request.POST,request.FILES)
		if(dataform.is_valid()):
			instance = dataform.save(commit = False)
			
			data_count = DataStore.objects.all().count()
			now = datetime.datetime.now().time()
			slug = 'data-'+str(data_count)+str(now)
			
			instance.slug = slug
			instance.save()

			return redirect('dashboard:dashboard-setup')

	else:
		dataform = DataForm()

	return render(request, 'dashboard/dashboard-setup.html', {'dataform':dataform,'avail_data':avail_data})

def dashboard_render(request,slug):

	data = DataStore.objects.get(slug=slug)

	df = pd.read_csv(data.data.path)
	df = df.drop(["id"],axis = 1)
	for index,row in df.iterrows():
		if(row['bedrooms']== 33):
			df = df.drop(index = index, axis = 1)

		inst = row['bathrooms']
		if(inst - int(inst)>= 0.5):
			inst = math.ceil(inst)
		else:
			inst = math.floor(inst)

		df.at[index,'bathrooms'] = inst
    
	df = df.dropna()
	count_row = df.shape[0]
	mean_price = round(df['price'].mean(),3)
	f,ax = plt.subplots(figsize=(20, 20))
	sns.heatmap(df.corr(), annot=True, linewidths=.2, fmt= '.3f',ax=ax).get_figure().savefig("static/heatmap.png")
	f,bx = plt.subplots(figsize=(15, 15))
	sns.lineplot(x="floors", y="price", data=df,ax=bx).get_figure().savefig("static/floors-price.png")
	fig_dims = (15, 10)
	fig, ax = plt.subplots(figsize=fig_dims)
	
	sns.barplot(x="grade", y="price", data=df,ax=ax).get_figure().savefig("static/grade-price.png")
	sns.barplot(x="condition", y="price", data=df,ax=ax).get_figure().savefig("static/condition-price.png")
	sns.barplot(x="view", y="price", data=df,ax=ax).get_figure().savefig("static/view-price.png")
	sns.barplot(x="bedrooms", y="price", data=df,ax=ax).get_figure().savefig("static/bedrooms-price.png")
	sns.barplot(x="bathrooms", y="price", data=df,ax=ax).get_figure().savefig("static/bathrooms-price.png")


	y = df['price']

	drop_list = ['view', 'yr_renovated','waterfront','date', 'price','zipcode','lat','long'] 
	X1 = df.drop(drop_list,axis=1)

	X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y, test_size = 1/3, random_state = 43)

	
	reg = XGBRegressor(n_estimators=100,learning_rate=.2)
	reg.fit(X1_train,y1_train)
	reg_score = round(reg.score(X1_train,y1_train),3)
	pred = reg.predict(X1_test)

	reg_score = reg_score*100
	rms = round(sqrt(mean_squared_error(y1_test, pred)),3)

	#df_show = df.to_html(max_rows=10)
	
	brand = str(data) + ' Dashboard'

	return render(request,'dashboard/dashboard-render.html',{'brand':brand,'data':data,'count_row':count_row,'mean_price':mean_price,'reg_score':reg_score,'rms':rms})


def dashboard_compute_pred(request):

	if(request.method == 'POST' and 'bedrooms' in request.POST and 'bathrooms' in request.POST and 'floors' in request.POST and 'condition' in request.POST and 'grade' in request.POST and 'sqft_living' in request.POST and 'sqft_lot' in request.POST and 'sqft_above' in request.POST and 'sqft_basement' in request.POST and 'sqft_living15' in request.POST and 'sqft_lot15' in request.POST and 'yr_built' in request.POST and 'data' in request.POST):
		
		bedrooms = request.POST['bedrooms']
		bedrooms = int(bedrooms)
		bathrooms = request.POST['bathrooms']
		bathrooms = int(bathrooms)
		floors = request.POST['floors']
		floors = int(floors)
		condition = request.POST['condition']
		condition = int(condition)
		grade = request.POST['grade']
		grade = int(grade)
		sqft_living = request.POST['sqft_living']
		sqft_living = int(sqft_living)
		sqft_lot = request.POST['sqft_lot']
		sqft_lot = int(sqft_lot)
		sqft_above = request.POST['sqft_above']
		sqft_above = int(sqft_above)
		sqft_basement = request.POST['sqft_basement']
		sqft_basement = int(sqft_basement)
		sqft_living15 = request.POST['sqft_living15']
		sqft_living15 = int(sqft_living15)
		sqft_lot15 = request.POST['sqft_lot15']
		sqft_lot15 = int(sqft_lot15)
		yr_built = request.POST['yr_built']
		yr_built = int(yr_built)
		temp = request.POST['data']

		test = {'bedrooms':bedrooms,'bathrooms':bathrooms,'sqft_living':sqft_living,'sqft_lot':sqft_lot,'floors':floors,'condition':condition,'grade':grade,'sqft_above':sqft_above,'sqft_basement':sqft_basement,'yr_built':yr_built,'sqft_living15':sqft_living15,'sqft_lot15':sqft_lot15}
		df_test=pd.DataFrame(test,index=[0])

		
		data = DataStore.objects.get(slug=temp)

		df = pd.read_csv(data.data.path)
	

		df = df.drop(["id"],axis = 1)
		for index,row in df.iterrows():
			if(row['bedrooms']== 33):
				df = df.drop(index = index, axis = 1)

			inst = row['bathrooms']
			if(inst - int(inst)>= 0.5):
				inst = math.ceil(inst)
			else:
				inst = math.floor(inst)

			df.at[index,'bathrooms'] = inst
	    
		df = df.dropna()
		
		y = df['price']

		drop_list = ['view', 'yr_renovated','waterfront','date', 'price','zipcode','lat','long'] 
		X1 = df.drop(drop_list,axis=1)

		X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y, test_size = 1/3, random_state = 43)

		
		reg = XGBRegressor(n_estimators=100,learning_rate=.2)
		reg.fit(X1_train,y1_train)
		result_pred = reg.predict(df_test)
		result_pred = float(result_pred)

		brand = str(data) + ' Dashboard'

		return render(request,'dashboard/dashboard-compute-pred.html',{'brand':brand,'data':data,'result_pred':result_pred,'bedrooms':bedrooms,'bathrooms':bathrooms,'floors':floors,'condition':condition,'grade':grade,'sqft_living':sqft_living,'sqft_lot':sqft_lot,'sqft_above':sqft_above,'sqft_basement':sqft_basement,'sqft_living15':sqft_living15,'sqft_lot15':sqft_lot15,'yr_built':yr_built})

	





