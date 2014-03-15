import csv, gspread, getpass

""" this python script downloads our google spreadsheet that all our data is in """
def update_cuisine(ingredients):
	#ingredient,category,cuisine
	email = raw_input("google email:")
	password = getpass.getpass("password:")
	client = gspread.login(email, password)
	docid = "0AiKU15z3fXFodFY1blNVR1FXTVRZbTRhbF9QQmd5X0E"
	spreadsheet = client.open_by_key(docid)
	[i,j] = [1,1]
	for [ingredient,category,cuisine] in ingredients:
		sheet = spreadsheet.worksheet(str(category))
		if category == False:
		#uncategorized, add to 'False' sheet
			sheet.update_cell(i,j,ingredient)
			i = i+1
			if i >99:
				[i,j] = [1,j+1]
		else:
		#categorized, update cuisine for category
			col_head = sheet.find(cuisine)
			row_head = sheet.find(ingredient)
			sheet.update_cell(row_head.row,col_head.col,'1')
		
	
def download():
	print "Sorry. Google email+pass required to pull csv's"

	email = raw_input("google email:")
	password = getpass.getpass("password:")

	client = gspread.login(email, password)
	docid = "0AiKU15z3fXFodFY1blNVR1FXTVRZbTRhbF9QQmd5X0E"
	spreadsheet = client.open_by_key(docid)

	for i, worksheet in enumerate(spreadsheet.worksheets()):
	    filename = str(worksheet)[12:-9] + '.csv'

	    with open("csv/"+filename, 'wb') as f:
    		writer = csv.writer(f)
    		writer.writerows(worksheet.get_all_values())
