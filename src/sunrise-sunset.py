from pygeocoder import Geocoder
import xml.etree.ElementTree as ET
import requests


# Assumption: All data inputs are actual locations, application does not include error handling


#convert city, country input into coordinates
#insert coordinates into url string
def coordinatesToURL(local):
    result = Geocoder.geocode(local)
    coords = str(result.coordinates)  # object returned ('xx.xxxx', 'xx.xxxx')
    coords_edit1 = coords.replace("(", "")  # remove opening parenthesis
    coords_edit2 = coords_edit1.replace(")", "")  # remove closing parenthesis
    lat_lon = coords_edit2.split(',')
    lat = lat_lon[0]
    lon = lat_lon[1].lstrip()  # remove white space
    url = "http://api.geonames.org/timezone?lat=" + lat + "&lng=" + lon + "&username=jdev5420"  # create url, insert coordinates
    return url


# function to convert time from 24hrs to AM/PM
def getTime(dateTime):
    time = dateTime[11:]  # isolate time from date time string
    hrs = int(dateTime[11:13])  # isolate hrs from time, cast as int
    if hrs > 12:
        adjTime = str(hrs - 12)  # adjust for 12hrs cycle, cast as string
        result = adjTime + dateTime[13:] + "pm"
    elif hrs == 12:
        result = time + "pm"
    elif hrs > 9:
        result = time + "am"
    else:
        noZero = str(hrs)  # remove leading zero by casting hrs to string
        result = noZero + dateTime[13:] + "am"
    return result


print("Welcome to the Sunrise / Sunset finder!")
location = input("Please enter a city, state, or country... ")

# url = coordinatesToURL(location)
r = requests.get(coordinatesToURL(location))  # return request from api.geonames.org
root = ET.fromstring(r.text)  # set root for XML doc
sunrise = root[0][9].text  # traverse children to sunrise tag
sunset = root[0][10].text  # traverse children to sunset tag

print("The sunrise is at " + getTime(sunrise) + " and the sunset is at " + getTime(sunset) + " local time in " + location + ".")