#! python
import sys, os, datetime
import numpy as np
import pandas as pd

def setup_filestructure(infile, infile2, outdatefile):
	if os.path.isfile(infile)==False:
		warnmsg = "No Input File Detected at :" + infile + ". Exiting."
		print(warnmsg)
		exit()


	if os.path.isfile(infile2) == False:
		warnmsg = "No Input File Deteccted at :" + infile2 + ". Exiting."
		print(warnmsg)
		exit()



	if os.path.isfile(outdatefile)==False:
		file = open(outdatefile,"w")
		file.close()
	else :
		file = open(outdatefile,"r+")
		file.seek(0)
		file.truncate()
		file.close

def validate_date(indate):
	indate_str=str(indate)
	try:
		d=datetime.datetime.strptime(indate,  '%m%d%Y')
		return(d.year)
	except ValueError:
		return(-1)

def check_zip(inzip):
	inzip_str=str(inzip)
	if (len(inzip_str) == 9):
		return(inzip_str[:5])
	elif (len(inzip_str) == 5):
		return(inzip_str)
	else:
		return(-1)

def donation_analysis(inputf, outputz, outputd):
	#initiate file paths
	scrdir = os.path.dirname(os.path.realpath('file'))
	input_file = os.path.abspath(os.path.realpath(os.path.join(scrdir,inputf)))
	input_file2 = os.path.abspath(os.path.realpath(os.path.join(scrdir, outputz)))
	outdatefile = os.path.abspath(os.path.realpath(os.path.join(scrdir, outputd)))
	#Setup file structure
	setup_filestructure(input_file,input_file2,outdatefile)
	#Check databank
	DB_header = ['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT','TRANSACTION_AMT']
	if ('DataBank' in vars()) == False:
		DataBank=pd.DataFrame(columns=DB_header)
		DataBank.TRANSACTION_AMT=DataBank.TRANSACTION_AMT.astype(float) #set to float
	#Read input file into dataframe
	header_1 = ["CMTE_ID","AMNDT_IND","RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP","ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER","OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID","TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID"]
	indata = pd.read_csv(input_file, sep="|", header = None, names = header_1,converters={'TRANSACTION_DT': lambda x: str(x),'ZIP_CODE': lambda x: str(x)})
	header_2 = ["percentile"]
	per = pd.read_csv(input_file2, names=header_2,converters={'percentile': lambda x: int(x)})
	#validate
	if (any(pd.isnull(indata.OTHER_ID)==False)):
		indata=indata[pd.isnull(indata.OTHER_ID)].reset_index(drop=True)
	if (any(pd.isnull(indata.CMTE_ID))):
		indata=indata[pd.isnull(indata.CMTE_ID)==False].reset_index(drop=True)
	if (any(pd.isnull(indata.TRANSACTION_AMT))):
		indata=indata[pd.isnull(indata.TRANSACTION_AMT)==False].reset_index(drop=True)
	if (any(pd.isnull(indata.NAME))):
		indata = indata[pd.isnull(indata.NAME) == False].reset_index(drop=True)


	for x in range(len(indata)):
		calc_zip = check_zip(indata.ZIP_CODE[x])
		calc_name = indata.NAME[x]
		calc_CMTE_ID = indata.CMTE_ID[x]
		calc_year = validate_date(indata.TRANSACTION_DT[x])
		in_per =per.iloc[0]['percentile']
		DataBank=DataBank.append(pd.DataFrame([[calc_CMTE_ID,calc_name,calc_zip,calc_year,indata.TRANSACTION_AMT[x]]],columns=DB_header),ignore_index=True)
		if int(calc_zip)>0: #check for zipcode
			ziptrans=DataBank.TRANSACTION_AMT[(DataBank.CMTE_ID==calc_CMTE_ID) & (DataBank.ZIP_CODE==calc_zip) & (DataBank.TRANSACTION_DT==2018)]
			if calc_year==2018:
				ziptrans_sort=ziptrans.sort_values()
				percent=ziptrans_sort.quantile(in_per/100,interpolation='nearest')
				num_fromzip=len(ziptrans_sort)
				tot_fromzip=np.sum(ziptrans_sort)
			#add data to file
			if calc_year==2018:
				file = open(outdatefile,"a")
				file.write(calc_CMTE_ID + '|' + str(calc_zip) + '|' + str(calc_year) + '|' + str(int(percent) ) + '|' + str(int(tot_fromzip)) + '|' + str(num_fromzip) + '\n')
				file.close()

if __name__== "__main__":
	donation_analysis(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))