# insights-data-engineering

Dependencies
Requires the following packages: pandas, numpy, datetime, os and sys

Run Command
python ./src/find_political_donors.py [INPUTFILES] [INPUTFILE2] [OUTPUTFILE]

python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

Or by using run.sh in main folder 'bash run.sh'

Input file
1. Calculations are done for this claendar year = 2018
2.Input file is expected to be pipe '|' separated with each line a new donation. Columns are in order: "CMTE_ID","AMNDT_IND","RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP","ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER","OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID","TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID"
