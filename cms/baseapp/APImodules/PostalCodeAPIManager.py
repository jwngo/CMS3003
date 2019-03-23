import json

with open('./baseapp/APImodules/postalcodes.json') as read_file:
	data = json.load(read_file)

def postal_code_to_latlong(postal_code):
	for location in data:
		if (location['POSTAL'] == postal_code):
			return location['LATITUDE'], location['LONGITUDE']

post_to_district_dict = {
	"01": ["01", "02", "03", "04", "05", "06"], 
  "02": ["07", "08"], 
  "03": ["14", "15", "16"], 
  "04": ["09", "10"], 
  "05": ["11", "12", "13"], 
  "06": ["17"], 
  "07": ["18", "19"],
  "08": ["20", "21"], 
  "09": ["22", "23"], 
  "10": ["24", "25", "26", "27"], 
  "11": ["28", "29", "30"],
  "12": ["31", "32", "33"], 
  "13": ["34", "35", "36", "37"], 
  "14": ["38", "39", "40", "41"], 
  "15": ["42", "43", "44", "45"], 
  "16": ["46", "47", "48"], 
  "17": ["49", "50", "81"], 
  "18": ["51", "52"], 
  "19": ["53", "54", "55", "82"],
  "20": ["56", "57"], 
  "21": ["58", "59"], 
  "22": ["60", "61", "62", "63", "64"], 
  "23": ["65", "66", "67", "68"], 
  "24": ["69", "70", "71"], 
  "25": ["72", "73"], 
  "26": ["77", "78"],
  "27": ["75", "76"],
  "28": ["79", "80"]
  }

district_to_area_dict = {
  "Raffles Place": "01",
  "Anson": "02",
  "Bukit Merah": "03",
  "Telok Blangah": "04",
  "Pasir Panjang": "05",
  "High Street": "06",
  "Middle Road": "07",
  "Little India": "08",
  "Orchard": "09",
  "Ardmore": "10",
  "Watten Estate": "11",
  "Balestier": "12",
  "Macpherson": "13",
  "Geyland": "14",
  "Katong": "15",
  "Bedok": "16",
  "Loyang": "17",
  "Simei": "18",
  "Serangoon Garden": "19",
  "Bishan": "20",
  "Upper Bukit Timah": "21",
  "Jurong": "22",
  "Hillview": "23",
  "Lim Chu Kang": "24",
  "Kranji": "25",
  "Upper Thomson": "26",
  "Yishun": "27",
  "Seletar": "28"
}

district_to_region_dict = {
	"Southwest": ["22", "23", "24"], 
  "Northwest": ["21","25", "26", "27",], 
  "Central": ["28", "20", "11", "10", "09", "05", "04", "03", "06", "02", "08", "07"],
  "Southeast": ["17", "16", "15", "12", "01"], 
  "Northeast": ["18", "19", "13", "14"]
  }


def postal_code_to_district(postalcode):
	postal_sector = postalcode[:2]
	for key, value in post_to_district_dict.items():
		if (postal_sector in value):
			return key

def district_to_region(postal_district):
	for key, value in district_to_region_dict.items():
		if (postal_district in value):
			return key


def postal_code_to_region(postal_code):
	postal_district = postal_code_to_district(postal_code)
	return district_to_region(postal_district)


def postal_code_to_area(postal_code):
  postal_district = postal_code_to_district(postal_code)
  for area, district in district_to_area_dict.items():
    if (postal_district in district):
      return area