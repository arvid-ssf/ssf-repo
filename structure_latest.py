import xlrd
import xlsxwriter
import pandas as pd


#--------NOTES--------
#pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc=sum, fill_value=0)




#--------------------







#--------read--------



#path="bra_statistik.xls"
#URGENT: MUST REWRITE THIS SO THAT YOU CAN ADD SHEETS WITH SAME DATES

def extract_column(x,nrows, inputWorksheet):
	column = []
	for y in range(6,nrows):
		#if inputWorksheet.cell_value(y,1) != "" or inputWorksheet.cell_value(y,0) == "4 kap. Brott mot frihet och frid": #hardcode, and second is because 4 kap has no number but needs to exists
		column.append(inputWorksheet.cell_value(y,x))
	return column


def read_file(file_name):
	inputWorkbook=xlrd.open_workbook(file_name, on_demand=True) #
	dic={}
	nrows=inputWorkbook.sheet_by_index(0).nrows 
	ncols=inputWorkbook.sheet_by_index(0).ncols 
	category_list = extract_column(0,nrows, inputWorkbook.sheet_by_index(0)) #default first sheet
	#Display error (upload output as input) if sheets have different lengths 

	for i in range(len(inputWorkbook.sheet_names())):
		inputWorksheet=inputWorkbook.sheet_by_index(i) #FOR LOOP

		region = inputWorksheet.cell_value(5,0)
		for x in range(1,ncols):
			year = inputWorksheet.cell_value(2,x)
			month = inputWorksheet.cell_value(3,x)
			if not year in dic:
				dic[year] = {}	
			if not month in dic[year]:
				dic[year][month]={}
			if not region in dic[year][month]:
				dic[year][month][region] = extract_column(x,nrows, inputWorksheet)
		

	#lots of blank cells: create category_list first time you save values			



	#--------write--------

	instance_1 = ["9 kap. Bedrägeri och annan oredlighet"]
	instance_2 = ["Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)", "Subventionsmissbruk, inkl. grovt (3 a §)", "Utpressning, ocker", "Häleri, häleriförseelse (6, 7 §)", ]
	instance_3 = ["Bedrägeri genom social manipulation (fr. o. m. 2019)","Identitetsbedrägeri (fr. o. m. 2019)","Fakturabedrägeri (fr. o. m. 2019)","Kortbedrägeri (fr. o. m. 2019)","Annonsbedrägeri (fr. o. m. 2019)", "Försäkringsbedrägeri (fr. o. m. 2019)", "Snyltningsbrott (fr. o. m. 2019)", "Grovt fordringsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)", "Automatmissbruk (t.o.m. 2018)", "Datorbedrägeri (t.o.m. 2018)", "Med kontokort (inte automatmissbruk) (t.o.m. 2018)", "Med hjälp av Internet (t.o.m. 2018)", "Investeringsbedrägeri (t.o.m. 2018)", "Överskrida eget konto (t.o.m. 2018)", "Mot försäkringsbolag (t.o.m. 2018)", "Mot EU:s finansiella intressen (t.o.m. 2018)", "Avs. husrum, förtäring, transport m.m. (t.o.m. 2018)", "Bedrägeri med hjälp av bluffaktura (t.o.m. 2018)", "Mot Försäkringskassan (t.o.m. 2007-07)", "Övrigt bedrägeri (t.o.m. 2018)", "Utpressning (4 §)", "Ocker (5 §)", "Penninghäleri, penninghäleriförseelse (t.o.m. 2014-06)", "Vanemässigt eller stor omfattning (6 §)", "Övrig häleri, häleriförseelse (7 §)"]
	instance_4 = ["Romansbedrägeri", "Investeringsbedrägeri", "Befogenhetsbedrägeri", "Annan typ", "Köp", "Lån", "Annan typ", "Med kontakt", "Utan kontakt", "Med fysiskt kort", "Utan fysiskt kort"] #, "Annonsbedrägeri", "Övrigt bedrägeri"  
	instance_5 = ["Internationell anknytning", "Ej internationell anknytning"]
	instance_6 = ["Mot äldre/funktionsnedsatt", "Ej mot äldre/funktionsnedsatt"]





								
	regions=["Hela landet","Region Nord","Region Mitt","Region Stockholm","Region Öst","Region Väst","Region Syd","Region Bergslagen"]
	crimes=["Bedrägeri genom social manipulation (fr. o. m. 2019)","Identitetsbedrägeri (fr. o. m. 2019)","Fakturabedrägeri (fr. o. m. 2019)","Kortbedrägeri (fr. o. m. 2019)","Annonsbedrägeri (fr. o. m. 2019)", "Försäkringsbedrägeri (fr. o. m. 2019)", "Snyltningsbrott (fr. o. m. 2019)", "Grovt fordringsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)", "Automatmissbruk (t.o.m. 2018)", "Datorbedrägeri (t.o.m. 2018)", "Med kontokort (inte automatmissbruk) (t.o.m. 2018)", "Med hjälp av Internet (t.o.m. 2018)", "Investeringsbedrägeri (t.o.m. 2018)", "Överskrida eget konto (t.o.m. 2018)", "Mot försäkringsbolag (t.o.m. 2018)", "Mot EU:s finansiella intressen (t.o.m. 2018)", "Avs. husrum, förtäring, transport m.m. (t.o.m. 2018)", "Bedrägeri med hjälp av bluffaktura (t.o.m. 2018)", "Mot Försäkringskassan (t.o.m. 2007-07)", "Övrigt bedrägeri (t.o.m. 2018)", ""]


	#create file
	outWorkbook = xlsxwriter.Workbook("strukturerad_tabell.xlsx")
	cell_format = outWorkbook.add_format()
	cell_format.set_pattern(1)  # This is optional when using a solid fill.
	cell_format.set_border(1)
	cell_format.set_bg_color('#C0C0C0')
	cell_format.set_border_color('#808080')

	#create worksheet
	outSheet = outWorkbook.add_worksheet("Samtliga (ostrukturerad)") 


	categories=["År","Region","Kategori","Tidsperiod","Antal"]	
	for i in range(len(categories)):
		outSheet.write(0,i,categories[i], cell_format)


	out_index = 1
	for year in dic:
		for month in dic[year]:
			for region in dic[year][month]:
				for i in range(0,len(dic[year][month][region])):
					if not dic[year][month][region][i] == "":
						outSheet.write(out_index,0,year)
						outSheet.write(out_index,1,region)
						outSheet.write(out_index,2,category_list[i])
						outSheet.write(out_index,3,month)		
						if not dic[year][month][region][i]=="..":
							outSheet.write(out_index,4,dic[year][month][region][i])
						elif dic[year][month][region][i]=="..":
							outSheet.write(out_index,4,"NaN")
						else:
							outSheet.write(out_index,4,dic[year][month][region][i])
						out_index += 1





	#---------------------------------------------------------SECOND SHEET----------------------------------------------------------

	#others = ["9 kap. Bedrägeri och annan oredlighet", "Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)"] #"8-12 kap. Brott mot förmögenhet", 
	sub_crimes = ["Romansbedrägeri", "Investeringsbedrägeri", "Befogenhetsbedrägeri", "Annan typ", "Köp", "Lån", "Annan typ", "Med kontakt", "Utan kontakt", "Med fysiskt kort", "Utan fysiskt kort"] #, "Annonsbedrägeri", "Övrigt bedrägeri"  
	geographical_connections = ["Internationell anknytning", "Ej internationell anknytning"]
	groups = ["Mot äldre/funktionsnedsatt", "Ej mot äldre/funktionsnedsatt"]
	missing_sub_crimes = ["Annonsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)", "Försäkringsbedrägeri (fr. o. m. 2019)", "Snyltningsbrott (fr. o. m. 2019)", "Grovt fordringsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)", "Automatmissbruk (t.o.m. 2018)", "Datorbedrägeri (t.o.m. 2018)", "Med kontokort (inte automatmissbruk) (t.o.m. 2018)", "Med hjälp av Internet (t.o.m. 2018)", "Investeringsbedrägeri (t.o.m. 2018)", "Överskrida eget konto (t.o.m. 2018)", "Mot försäkringsbolag (t.o.m. 2018)", "Mot EU:s finansiella intressen (t.o.m. 2018)", "Avs. husrum, förtäring, transport m.m. (t.o.m. 2018)", "Bedrägeri med hjälp av bluffaktura (t.o.m. 2018)", "Mot Försäkringskassan (t.o.m. 2007-07)", "Övrigt bedrägeri (t.o.m. 2018)", "Utpressning (4 §)", "Ocker (5 §)", "Penninghäleri, penninghäleriförseelse (t.o.m. 2014-06)", "Vanemässigt eller stor omfattning (6 §)", "Övrig häleri, häleriförseelse (7 §)"] # (fr. o. m. 2019) kolla när du tar bort denna string




	instance_1 = ["9 kap. Bedrägeri och annan oredlighet"]
	instance_2 = ["Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)", "Subventionsmissbruk, inkl. grovt (3 a §)", "Utpressning, ocker", "Häleri, häleriförseelse (6, 7 §)", ]
	#instance_3 kan den innefatta allt from instance_2 eller måste den delas upp?
	instance_3 = ["Bedrägeri genom social manipulation (fr. o. m. 2019)","Identitetsbedrägeri (fr. o. m. 2019)","Fakturabedrägeri (fr. o. m. 2019)","Kortbedrägeri (fr. o. m. 2019)","Annonsbedrägeri (fr. o. m. 2019)", "Försäkringsbedrägeri (fr. o. m. 2019)", "Snyltningsbrott (fr. o. m. 2019)", "Grovt fordringsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)", "Automatmissbruk (t.o.m. 2018)", "Datorbedrägeri (t.o.m. 2018)", "Med kontokort (inte automatmissbruk) (t.o.m. 2018)", "Med hjälp av Internet (t.o.m. 2018)", "Investeringsbedrägeri (t.o.m. 2018)", "Överskrida eget konto (t.o.m. 2018)", "Mot försäkringsbolag (t.o.m. 2018)", "Mot EU:s finansiella intressen (t.o.m. 2018)", "Avs. husrum, förtäring, transport m.m. (t.o.m. 2018)", "Bedrägeri med hjälp av bluffaktura (t.o.m. 2018)", "Mot Försäkringskassan (t.o.m. 2007-07)", "Övrigt bedrägeri (t.o.m. 2018)", "Utpressning (4 §)", "Ocker (5 §)", "Penninghäleri, penninghäleriförseelse (t.o.m. 2014-06)", "Vanemässigt eller stor omfattning (6 §)", "Övrig häleri, häleriförseelse (7 §)"]
	instance_4 = ["Romansbedrägeri", "Investeringsbedrägeri", "Befogenhetsbedrägeri", "Annan typ", "Köp", "Lån", "Annan typ", "Med kontakt", "Utan kontakt", "Med fysiskt kort", "Utan fysiskt kort"] #, "Annonsbedrägeri", "Övrigt bedrägeri"  
	instance_5 = ["Internationell anknytning", "Ej internationell anknytning"]
	instance_6 = ["Mot äldre/funktionsnedsatt", "Ej mot äldre/funktionsnedsatt"]


	



	outSheet2 = outWorkbook.add_worksheet("Fr. o. m. 2019 (månader)")

	categories=["År","Region","Brottskategori","Brottstyp","Geografisk anknytning","Målgrupp","Tidsperiod","Antal"]	
	for i in range(len(categories)):
		outSheet2.write(0,i,categories[i], cell_format)


	month_dic ={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'Maj':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Okt':10, 'Nov':11, 'Dec':12}
	out_index = 1
	for year in dic:
		for month in dic[year]:
			for region in dic[year][month]:
				for i in range(0,len(dic[year][month][region])):
					if not dic[year][month][region][i] == "":
						if category_list[i] in crimes:
							crime = category_list[i]
							if crime in missing_sub_crimes:
								sub_crime = crime
						elif category_list[i] in geographical_connections:
							geographical_connection = category_list[i]
						elif category_list[i] in sub_crimes:
							if category_list[i] == "Annan typ":
								sub_crime = category_list[i] + " (" + crime + ")"
							else:
								sub_crime = category_list[i]
						#elif category_list[i] in others:
						#	continue
						elif category_list[i] in groups:
							if month != 'Helår':
								group = category_list[i]
								if 'prel.' in year:
									year_rewritten = year.replace(' prel.', '')
									outSheet2.write(out_index,0,year_rewritten)
								else:
									outSheet2.write(out_index,0,year)
								outSheet2.write(out_index,1,region)
								outSheet2.write(out_index,2,crime)
								outSheet2.write(out_index,3,sub_crime)
								outSheet2.write(out_index,4,geographical_connection)
								outSheet2.write(out_index,5,group)
								outSheet2.write(out_index,6,month_dic[month])
								if not dic[year][month][region][i]=="..":
									outSheet2.write(out_index,7,dic[year][month][region][i])
								elif dic[year][month][region][i]=="..":
									outSheet2.write(out_index,7,"NaN")
								else:
									outSheet2.write(out_index,7,dic[year][month][region][i])
								out_index += 1


							




						 											
					




			

	




	#---------------------------------------------------------THRID SHEET----------------------------------------------------------


	outSheet3 = outWorkbook.add_worksheet("Fr. o. m. 2019 (helår)")

	categories_whole_year =["År","Region","Brottskategori","Brottstyp","Geografisk anknytning","Målgrupp","Antal"]	
	for i in range(len(categories_whole_year)):
		outSheet3.write(0,i,categories_whole_year[i], cell_format)

	static_month = "Helår"
	out_index = 1
	for year in dic:
		if static_month in dic[year]:
			for region in dic[year][static_month]:
				for i in range(0,len(dic[year][static_month][region])):
					if not dic[year][static_month][region][i] == "":
						if category_list[i] in crimes:
							crime = category_list[i] 
							#crime = crime.replace(' (fr. o. m. 2019)','') #remove fr. o. m. 2019
							if crime in missing_sub_crimes:
								sub_crime = crime#"-" 											
						elif category_list[i] in geographical_connections:
							geographical_connection = category_list[i]
						elif category_list[i] in sub_crimes:
							if category_list[i] == "Annan typ":
								sub_crime = category_list[i] + " (" + crime + ")"
							else:
								sub_crime = category_list[i]
						#elif dic["Brott"][i] in others:
						#	continue
						elif category_list[i] in groups:
							group = category_list[i]
							outSheet3.write(out_index,0,year) #CHANGE TO STR?
							outSheet3.write(out_index,1,region)
							outSheet3.write(out_index,2,crime)
							outSheet3.write(out_index,3,sub_crime)
							outSheet3.write(out_index,4,geographical_connection)
							outSheet3.write(out_index,5,group)
							if not dic[year][static_month][region][i]=="..":
								outSheet3.write(out_index,6,dic[year][static_month][region][i])
							elif dic[year][static_month][region][i]=="..":
								outSheet3.write(out_index,6,"NaN")
							else:
								outSheet3.write(out_index,6,dic[year][static_month][region][i])
							out_index += 1



	#---------------------------------------------------------FOURTH SHEET----------------------------------------------------------


	others = ["8-12 kap. Brott mot förmögenhet", "9 kap. Bedrägeri och annan oredlighet", "Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)"]
	sub_crimes = ["Romansbedrägeri", "Investeringsbedrägeri", "Befogenhetsbedrägeri", "Annan typ", "Köp", "Lån", "Annan typ", "Med kontakt", "Utan kontakt", "Med fysiskt kort", "Utan fysiskt kort"]  
	geographical_connections = ["Internationell anknytning", "Ej internationell anknytning"]
	groups = ["Mot äldre/funktionsnedsatt", "Ej mot äldre/funktionsnedsatt"]
	missing_sub_crimes = ["Annonsbedrägeri (fr. o. m. 2019)", "Övrigt bedrägeri (fr. o. m. 2019)"]


	

	outSheet4 = outWorkbook.add_worksheet("Fr. o. m. 2019 (helår|månader)")
	
	#2020 do not have whole year
	categories_by_month =["År","Region","Brottskategori","Brottstyp","Geografisk anknytning","Målgrupp", "Helår", "Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep","Okt","Nov","Dec"]	
	for i in range(len(categories_by_month)):
		outSheet4.write(0,i,categories_by_month[i], cell_format)

	static_month = "Helår"
	out_index = 1
	#start = out_index
	#month_index = 6#5 #place for Jan (+1 in first loop since "" is first element of key_list) 
	#start_year = 2015 #do not want ""

	for year in dic:
		start = out_index
		if static_month in dic[year]:
			month_index = 6
		else:
			month_index = 7

		for month in dic[year]:
			out_index = start
			for region in dic[year][month]:
				for i in range(0,len(dic[year][month][region])):
					if not dic[year][month][region][i] == "":
						if category_list[i] in crimes:
							crime = category_list[i]
							#crime = crime.replace(' (fr. o. m. 2019)','')
							if crime in missing_sub_crimes:
								sub_crime = crime#"-"
						elif category_list[i] in geographical_connections:
							geographical_connection = category_list[i]
						elif category_list[i] in sub_crimes:
							if category_list[i] == "Annan typ":
								sub_crime = category_list[i] + " (" + crime + ")"
							else:
								sub_crime = category_list[i]
						#elif dic["Brott"][i] in others:
						#	continue
						elif category_list[i] in groups:
							group = category_list[i]
							outSheet4.write(out_index,0,year)
							outSheet4.write(out_index,1,region)
							outSheet4.write(out_index,2,crime)
							outSheet4.write(out_index,3,sub_crime)
							outSheet4.write(out_index,4,geographical_connection)
							outSheet4.write(out_index,5,group)
							if not dic[year][month][region][i]=="..":
								outSheet4.write(out_index,month_index,dic[year][month][region][i])
							elif dic[year][month][region][i]=="..":
								outSheet4.write(out_index,month_index,"NaN") 
							else:
								outSheet4.write(out_index,month_index,dic[year][month][region][i])

							if static_month not in dic[year] and month_index == 7:
								outSheet4.write(out_index,6,"NaN")

							out_index += 1
			month_index +=1		

			
	#write Nan

		



#---------------------------------------------------------FIFTH SHEET----------------------------------------------------------

#HUR KATEGORISERA.....
	
	chapters = ["4 kap. Brott mot frihet och frid", "9 kap. Bedrägeri och annan oredlighet"]
	paragraphs = ["Dataintrång (9 c §)", "Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)", "Subventionsmissbruk, inkl. grovt (3 a §)", "Utpressning, ocker", "Häleri, häleriförseelse (6, 7 §)", "Övriga brott mot 9 kap. (3 a, 8-10 §)"]
	regions=["Hela landet","Region Nord","Region Mitt","Region Stockholm","Region Öst","Region Väst","Region Syd","Region Bergslagen"]

	outSheet5 = outWorkbook.add_worksheet("Kapitel (helår)")

	categories_whole_year =["År","Region", "Kapitel", "Paragraf", "Antal"]	
	for i in range(len(categories_whole_year)):
		outSheet5.write(0,i,categories_whole_year[i], cell_format)

	out_index = 1


	

	static_month = "Helår"
	out_index = 1
	for year in dic:
		if static_month in dic[year]:
			for region in dic[year][static_month]:
				for i in range(0,len(dic[year][static_month][region])):
					if not dic[year][static_month][region][i] == "" or category_list[i] == "4 kap. Brott mot frihet och frid": #since it has no value
						if category_list[i] in chapters:
							chapter = category_list[i]
						elif category_list[i] in paragraphs:
							paragraph = category_list[i] 
							outSheet5.write(out_index,0,year) #CHANGE TO STR?
							outSheet5.write(out_index,1,region)
							outSheet5.write(out_index,2,chapter)
							outSheet5.write(out_index,3,paragraph)
							if not dic[year][static_month][region][i]=="..":
								outSheet5.write(out_index,4,dic[year][static_month][region][i])
							elif dic[year][static_month][region][i]=="..":
								outSheet5.write(out_index,4,"NaN")
							else:
								outSheet5.write(out_index,4,dic[year][static_month][region][i])
							out_index += 1
					
					


	#---------------------------------------------------------SIXTH SHEET----------------------------------------------------------

	chapters = ["4 kap. Brott mot frihet och frid", "9 kap. Bedrägeri och annan oredlighet"]
	paragraphs = ["Dataintrång (9 c §)", "Bedrägeri inkl. grovt, bedrägligt beteende (1-3 §)", "Subventionsmissbruk, inkl. grovt (3 a §)", "Utpressning, ocker", "Häleri, häleriförseelse (6, 7 §)", "Övriga brott mot 9 kap. (3 a, 8-10 §)"]
	
	outSheet6 = outWorkbook.add_worksheet("Kapitel (månader)")

	categories =["År","Region", "Kapitel", "Paragraf", "Tidsperiod", "Antal"]
	for i in range(len(categories)):
		outSheet6.write(0,i,categories[i], cell_format)

	
	month_dic ={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'Maj':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Okt':10, 'Nov':11, 'Dec':12}
	out_index = 1

	for year in dic:
		for month in dic[year]:
			for region in dic[year][month]:
				for i in range(0,len(dic[year][month][region])):
					if not dic[year][month][region][i] == "" or category_list[i] == "4 kap. Brott mot frihet och frid": 
						if category_list[i] in chapters:
							chapter = category_list[i]
						elif category_list[i] in paragraphs:										
							if month != 'Helår':
								paragraph = category_list[i]
								if 'prel.' in year:
									year_rewritten = year.replace(' prel.', '')
									outSheet6.write(out_index,0,year_rewritten)
								else:
									outSheet6.write(out_index,0,year)
								outSheet6.write(out_index,1,region)
								outSheet6.write(out_index,2,chapter)
								outSheet6.write(out_index,3,paragraph)
								outSheet6.write(out_index,4,month_dic[month])							
								if not dic[year][month][region][i]=="..":
									outSheet6.write(out_index,5,dic[year][month][region][i])
								elif dic[year][month][region][i]=="..":
									outSheet6.write(out_index,5,"NaN")
								else:
									outSheet6.write(out_index,5,dic[year][month][region][i])
								out_index += 1





	outWorkbook.close()


	#convert excel to csv

	 
	excel_file = "strukturerad_tabell.xlsx"
           
    #pickle                                                               
	# df1 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår") 
	# df1.to_pickle("pickle/df1.pkl")
	# df2 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader")
	# df2.to_pickle("pickle/df2.pkl")
	# #df3 = pd.read_excel(excel_file,sheet_name='Strukturerad_per_månad') #Wrong: JAN ends up under 'Helår' year 2020
	# df4 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår_Total")
	# df4.to_pickle("pickle/df4.pkl")
	# df5 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader_Total")
	# df5.to_pickle("pickle/df5.pkl")


	#feather (works in R as well)
	df1 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (helår)") 
	df1.to_feather("feather/df1.feather")
	df2 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (månader)")
	df2.to_feather("feather/df2.feather")
	df3 = pd.read_excel(excel_file,sheet_name="Fr. o. m. 2019 (helår|månader)") #Wrong: JAN ends up under 'Helår' year 2020
	df3.to_feather("feather/df3.feather")
	df4 = pd.read_excel(excel_file,sheet_name="Kapitel (helår)")
	df4.to_feather("feather/df4.feather")
	df5 = pd.read_excel(excel_file,sheet_name="Kapitel (månader)")
	df5.to_feather("feather/df5.feather")


	#hdf5 (install tables)
	# df1 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår") 
	# df1.to_hdf("hdf5/df1.h5", key='df')
	# df2 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader")
	# df2.to_hdf("hdf5/df2.h5", key='df')
	# #df3 = pd.read_excel(excel_file,sheet_name='Strukturerad_per_månad') #Wrong: JAN ends up under 'Helår' year 2020
	# df4 = pd.read_excel(excel_file,sheet_name="Strukturerad_Helår_Total")
	# df4.to_hdf("hdf5/df4.h5", key='df')
	# df5 = pd.read_excel(excel_file,sheet_name="Strukturerad_Månader_Total")
	# df5.to_hdf("hdf5/df5.h5", key='df')




		
#read_file("bra_statistik_regioner.xls")


