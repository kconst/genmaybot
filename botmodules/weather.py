import urllib2, urllib, xml.dom.minidom

def get_weather( zip):
    #google weather of place specified in 'zip'

       url = "http://www.google.com/ig/api?weather=" + urllib.quote(zip)
       dom = xml.dom.minidom.parse(urllib2.urlopen(url))
       
       if not dom.getElementsByTagName('problem_cause'):
           city = dom.getElementsByTagName('city')[0].getAttribute('data')
           temp_f = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_f')[0].getAttribute('data')
           temp_c = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_c')[0].getAttribute('data')
           try:
            humidity = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('humidity')[0].getAttribute('data')
           except:
            humidity = ""
           
           try: 
            wind = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('wind_condition')[0].getAttribute('data')
           except:
            wind = "" 
            
           try:
            condition = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('condition')[0].getAttribute('data')
           except:
            condition = "" 
           
           degree_symbol = unichr(176)
           
           chanmsg = "%s / %s / %s%sF %s%sC / %s / %s" % (city, condition, temp_f,degree_symbol, temp_c, degree_symbol, humidity, wind)
           chanmsg = chanmsg.encode('utf-8')
       else:
           chanmsg = get_weather2(zip)
       
       return chanmsg

get_weather.command = "!w"
   
def get_weather2(zip):
    #wunderground weather of place specified in 'zip'
        url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=" + urllib.quote(zip)
        dom = xml.dom.minidom.parse(urllib2.urlopen(url))
        city = dom.getElementsByTagName('display_location')[0].getElementsByTagName('full')[0].childNodes[0].data
        if city != ", ":
            temp_f = dom.getElementsByTagName('temp_f')[0].childNodes[0].data
            temp_c = dom.getElementsByTagName('temp_c')[0].childNodes[0].data
            try:
                condition = dom.getElementsByTagName('weather')[0].childNodes[0].data
            except:
                condition = ""
            try:
                humidity = "Humidity: " + str(dom.getElementsByTagName('relative_humidity')[0].childNodes[0].data)
            except:
                humidity = ""
            try:
                wind = "Wind: " + str(dom.getElementsByTagName('wind_string')[0].childNodes[0].data)
            except:
                humidity = ""
            
            degree_symbol = unichr(176)
            chanmsg = "%s / %s / %s%sF %s%sC / %s / %s" % (city, condition, temp_f,degree_symbol, temp_c, degree_symbol, humidity, wind)
            chanmsg = chanmsg.encode('utf-8')
            return chanmsg

get_weather2.command = "!wu"