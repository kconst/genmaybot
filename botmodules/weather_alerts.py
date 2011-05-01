import urllib2, xml.dom.minidom, datetime, botmodules.tools as tools
from dateutil.parser import parse as dateparser


def weather_alert():
  try:
    latest_update, latest_entry, alert_url = find_latest_weather_alert()
    ago = (datetime.datetime.utcnow() - latest_update).seconds/60
    
    if not weather_alert.lastcheck:
      weather_alert.lastcheck = latest_update
    if latest_update > weather_alert.lastcheck:
      weather_alert.lastcheck = latest_update
      return get_weather_alert_data(alert_url)
      
  except Exception as inst:
    print "weather_alert: " + str(inst)
    pass    

weather_alert.alert=True
weather_alert.lastcheck=""

def find_latest_weather_alert():
  try:
    request = urllib2.urlopen("http://alerts.weather.gov/cap/us.php?x=1")
    dom = xml.dom.minidom.parse(request)
    latest_update = datetime.datetime(1970,1,1) ## for comparing against the latest weather entry

    ## this is all necessary because the government didn't feel like sorting the XML feed
    ## so the timestamps are all over the place. We have to find the latest entry ourselves
    weather_entries = dom.getElementsByTagName('entry')
    cur_entry = 0

    for entry in weather_entries:
      updated = entry.getElementsByTagName('updated')[0].childNodes[0].data  
      updated = dateparser(updated)
      updated = (updated - updated.utcoffset()).replace(tzinfo=None)
      cur_entry+=1
      
      if latest_update < updated:
        latest_update = updated
        latest_entry = cur_entry
        alert_url = entry.getElementsByTagName('id')[0].childNodes[0].data 
        
    return latest_update, latest_entry, alert_url
  except Exception as inst:
    print "find_latest_weather_alert: " + str(inst)
    pass    


def get_weather_alert_data(alert_url):
  try:
    request = urllib2.urlopen(alert_url)
    dom = xml.dom.minidom.parse(request)
    msgType = dom.getElementsByTagName('msgType')[0].childNodes[0].data
    note = dom.getElementsByTagName('note')[0].childNodes[0].data
    event = dom.getElementsByTagName('event')[0].childNodes[0].data
    urgency = dom.getElementsByTagName('urgency')[0].childNodes[0].data
    severity = dom.getElementsByTagName('severity')[0].childNodes[0].data
    certainty = dom.getElementsByTagName('certainty')[0].childNodes[0].data
    updated = dom.getElementsByTagName('sent')[0].childNodes[0].data

    updated = dateparser(updated)
    updated = (updated - updated.utcoffset()).replace(tzinfo=None)
    ago = (datetime.datetime.utcnow() - updated).seconds/60


    short_url = tools.shorten_url(alert_url)
    alert_text = "[Weather] %s: %s Urgency: %s Severity: %s Certainty: %s | %s (%s minutes ago)" % (msgType, event, urgency, severity, certainty, note[0:150], ago)
    
    
    return "%s [ %s ]" % (alert_text, short_url)
  except Exception as inst:
    print "get_weather_alert_data: " + str(inst)
    pass    

  
def get_weather_alert(self, e):
## find latest weather alert and displays it
  latest_update, latest_entry, alert_url = find_latest_weather_alert()
  e.output = get_weather_alert_data(alert_url)
  return e
  
get_weather_alert.command = "!wa"
get_weather_alert.helptext = "Usage: !wa\nShows the latest weather alert from http://alerts.weather.gov"
  