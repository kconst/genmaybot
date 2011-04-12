import urllib2, botmodules.tools as tools

def get_fml(nothing):  
  try:
    fmlxml = urllib2.urlopen("http://api.betacie.com/view/random?key=%s&language=en" % tools.config.fmlAPIkey).read()
    start = fmlxml.find("<text>") + 6
    end = fmlxml.find("</text>")
    
    fml = fmlxml[start:end]
    
    start = fmlxml.find("<agree>") + 7
    end = fmlxml.find("</agree>")
    
    fml = fml + " [FYL: " + str(fmlxml[start:end])
    
    start = fmlxml.find("<deserved>") + 10
    end = fmlxml.find("</deserved>")   
    
    fml = fml + " Deserved it: " + str(fmlxml[start:end]) + "]"
    
    
    fml = fml.replace('&quot;', '"')
    fml = fml.replace('&amp;quot;', '"')
    fml = fml.replace('&amp;', "&")
    fml = tools.decode_htmlentities(fml)
    
    return fml
  except Exception as inst:
    print "!fml " + str(inst)
    return
get_fml.command = "!fml"