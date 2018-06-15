from collections import defaultdict
import os
import xlrd

STATION_TO_DISTRICT = {
	"RM": 7,
	"EN": [3, 7],
	"EP": [3, 7],
	"NB": 3,
	"BK": 3,
	"AS": 7,
	"MA": [4, 7],
	"19": 4,
	"12": 4,
	"LM": 4,
	"FV": 4,
	"CL": 4,
	"SL": 3,
	"BF": 0,
	"HY": 5,
	"SH": 6,
	"UC": 6,
	"FM": 6,
	"CN": 1,
	"PH": 1,
	"WC": 1,
	"LF": 1,
	"OR": 3,
	"RR": 3,
	"OW": 7,
	"EM": [7, 8],
	"MT": [7, 8],
	"PL": 9,
	"CC": 9,
	"16": 9,
	"24": 9,
	"GP": 9,
	"BP": [8, 9],
	"DC": 0,
	"CM": 0,
	"CV": 5,
	"ED": 5,
	"NC": 2,
	"WP": 2,
	"SS": 0,
	"SB": 0,
	"SO": 0,
	"MB": 0,
	"WD": 5,
	"OA": 4,
	"WS": 6
}

DISTRICT_TO_REP = {
	0: "None",
	1: "Debora Allen",
	2: "Joel Keller",
	3: "Rebecca Saltzman",
	4: "Robert Raburn",
	5: "John McPartland",
	6: "Thomas Blalock",
	7: "Lateefah Simon",
	8: "Nick Josefowitz",
	9: "Bevan Dufty"
}

DATA_DIR = "2018/"

workbook = xlrd.open_workbook("key.xls")
sheet = workbook.sheet_by_index(0)

station_keys = {}
for row_idx in range(1, sheet.nrows):
    cols = sheet.row_values(row_idx)
    station_keys[str(cols[1])] = str(cols[2])


counts = defaultdict(float)
total = 0.0

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

for filename in listdir_nohidden(DATA_DIR):
	workbook = xlrd.open_workbook(DATA_DIR + filename)
	for sheet_idx in [0, 1, 2]:
		sheet = workbook.sheet_by_index(sheet_idx)
		stations = sheet.row_values(1)
		totals = sheet.row_values(sheet.nrows - 1)
		for col_idx in range(1, sheet.ncols - 1):
			total += float(totals[col_idx])
			if isinstance(stations[col_idx], float):
				counts[str(int(stations[col_idx]))] += float(totals[col_idx])
			else:
				counts[str(stations[col_idx])] += float(totals[col_idx])

count_by_districts = defaultdict(float)

for k, v in counts.iteritems():
	if str(k) not in STATION_TO_DISTRICT:
		# TODO: Figure out WTF is up here.
		continue
	districts = STATION_TO_DISTRICT[k]
	if isinstance(districts, list):
		for district in districts:
			count_by_districts[district] += float(v / len(districts))
	else:
		count_by_districts[districts] += v

for k, v in count_by_districts.iteritems():
	pct = float(v / total) * 100
	if k == 0:
		print("Approximately %.2f%% of riders aren't represented on the BART Board" % pct)
	else:
		print("Approximately %.2f%% of riders are in District %i" % (pct, k))
