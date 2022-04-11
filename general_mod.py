import pandas as pd
import datetime
from datetime import timedelta
import numpy as np
from variables_mod import *

from library import (
	ExcelWriter
)



																
def cleaning_data (df):
	
	df = df.apply(lambda x: x.str.strip())
	df.columns = df.columns.str.strip()
	df = df.replace(r'^\s*$', np.nan, regex=True)
	#valid_data = df[df.notnull().all(axis =1)]
	#invalid_data = df[df.isnull().any(axis =1)]
	
	return (df)
	
	
def weekly_date (df, series_dates):

	for val in series_dates:
	
		df[val] = pd.to_datetime(df[val], dayfirst = True)
		df['week_day_temp'] = df[val].apply(lambda x: x.weekday())
		df[val] = df[val] - df['week_day_temp'] * timedelta(days=1) 
		df.drop (['week_day_temp'], axis = 1,inplace = True)
	
	return df
	
	
	
def asign_weeks (df, begin_date, end_date, name_new_serie = 'WEEKS_EVENT'):
	
	for ind, row in df.iterrows():
		valuesWeeks = []
		valuesNew_str = {}
		weekly_begin = row[begin_date].date()
		weekly_end = row[end_date].date()
		
		if weekly_begin <= weekly_end:
			while weekly_begin <= weekly_end:
				
				if weekly_begin == weekly_end:
					add_week = weekly_begin.strftime("%Y-%m-%d")
					valuesWeeks.append(add_week)
					valuesNew_str = ','.join(valuesWeeks)
					weekly_begin = weekly_begin + datetime.timedelta(days=7)
					df.loc[ind,name_new_serie] = valuesNew_str
				else:
					add_week = weekly_begin.strftime("%Y-%m-%d")
					valuesWeeks.append(add_week)
					weekly_begin = weekly_begin + datetime.timedelta(days=7)
					valuesNew_str = ','.join(valuesWeeks)
					df.loc[ind,name_new_serie] = valuesNew_str
		else:
			df.loc[ind,name_new_serie] = 'BeginDate > EndDate'
	
	df_valid = df[df[name_new_serie] != 'BeginDate > EndDate']
	df_valid.drop([begin_date, end_date], axis = 1,inplace = True)
	
	return df_valid
	

def group_entities(df, list_series, sep = ',', sort_flag = True):
	
	df = df.applymap(str)
	df.set_index (list_series, inplace=True)
	df = df.groupby (level = list_series, sort = sort_flag).agg(sep.join)
	df.reset_index(inplace=True)
	return df
	
	
def group_unique_entities(df, list_series, sep = ','):

	df = df.applymap(str)
	df.set_index (list_series, inplace=True)
	df = df.groupby (level = list_series, sort=True).agg(lambda x:sep.join(x.unique()))
	df.reset_index(inplace=True)

	return df  
	
	
def extract_numeric_values (df, name_serie):
	#regex => find any digits on String '(\d+)'
	# '([1-9]\d{3,})' => 4 or more digits   
	df = df.copy()
	df[name_serie] = df [name_serie].str.findall('([1-9]\d{3,})').apply(','.join)
	
	return df   


def write_file(df, path_associad, sheet_name_associad):
    
    with ExcelWriter(path_associad, engine = 'openpyxl', mode='a') as writer:  
        df.to_excel(writer, sheet_name=sheet_name_associad,index = False, freeze_panes=(1,0))
		

	
def split_by_column(column,sep):
	
	return pd.Series(column.str.cat(sep=sep).split(sep=sep))
	
	
def split_by_rows(df, name_serie, sep): 
 
	df= df.applymap(str)
	df_new = (df.groupby(df.columns.drop(name_serie).tolist()) 
	[name_serie]
	.apply(split_by_column,sep=sep) 
	.reset_index(drop=True,level=-1).reset_index()) 
	
	return df_new
	

def range_int (x, y):
	
	x = int(x)
	y = int (y)
	range_slots = list(range(x, y))
	range_slots = [str(x) for x in range_slots]
	values_range = ','.join(range_slots)
	
	return values_range




	
	
	
