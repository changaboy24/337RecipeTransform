import csv, gspread, getpass,re

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

download()