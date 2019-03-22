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

district_to_region_dict = {
        "Southwest": ["22", "23", "24"], 
        "Northwest": ["21","25", "26", "27",], 
        "Central": ["28", "20", "11", "10", "9", "5", "4", "3", "6", "2", "8", "7"],
        "Southeast": ["17", "16", "15", "12", "1"], 
        "Northeast": ["18", "19", "13", "14"]
        }


        


def post_to_postal_district(postalcode): 
    postal_sector = postalcode[:2] 
    for key, value in post_to_district_dict.items(): 
        if(postal_sector in value):
            return key

def postal_district_to_region(postaldistrict):
    for key, value in district_to_region_dict.items(): 
        if(postaldistrict in value): 
            return key


postaldistrict = (post_to_postal_district(str(603286)))
print(postal_district_to_region(postaldistrict))
