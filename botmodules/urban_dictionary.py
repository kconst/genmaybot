

def get_urbandictionary(self, e):
    searchterm = e.input
    url = "http://www.urbandictionary.com/define.php?term=%s" % searchterm

    if searchterm == "wotd":
        e.output = get_urbandictionary_wotd(self)
        return e

    if searchterm == "":
        url = "http://www.urbandictionary.com/random.php"

    page = self.tools["load_html_from_URL"](url)

    first_definition = ""

    if page.find(id='not_defined_yet') != None:
        return None

## depending on the search results the first word may be contained directly under the <td class='word'> tag
## or it may be the text contents of a <a href> tag
## we first try to get it from inside a <td><a href>[word]</a></td> type structure
## if that fails, get the word under the initial <td> tag

    try:
        first_word = page.findAll('td', attrs={"class": "word"})[0].contents[1].string
    except:
        first_word = page.findAll('td', attrs={"class": "word"})[0].contents[0].string

    first_word = first_word.replace("\n", "")

    for content in page.findAll('div', attrs={"class": "definition"})[0].contents:
        if content.string != None:
            first_definition += content.string

    #first_definition = first_definition.encode("utf-8", 'ignore')
#    first_definition = tools.decode_htmlentities(first_definition)
#    first_word = tools.decode_htmlentities(first_word)

    first_definition = first_definition.replace("\n", " ")
    first_definition = first_definition.replace("\r", " ")
    first_definition = first_definition[0:392]

    first_definition = ((first_word + ": " + first_definition) + " [ %s ]" % self.tools['shorten_url'](url))
    #print first_definition
    e.output = first_definition
    return e

get_urbandictionary.command = "!ud"
get_urbandictionary.helptext = "Usage: !ud <word or phrase>\nExample: !ud hella\nShows urbandictionary definition of a word or phrase.\n!ud alone returns a random entry\n!ud wotd returns the current word of the day"


def get_urbandictionary_wotd(self):

    url = "http://www.urbandictionary.com"
    page = self.tools["load_html_from_URL"](url)
    first_definition = ""

    first_word = page.findAll('div', attrs={"class": "word"})[0].contents[1].contents[0].string
    first_word = first_word.encode("utf-8", 'ignore')

    for content in page.findAll('div', attrs={"class": "definition"})[0].contents:
        if content.string != None:
            first_definition += content.string

#    first_definition = tools.decode_htmlentities(first_definition)
    first_definition = first_definition.replace("\n", " ")

    wotd = (first_word.decode('utf-8') + ": " + first_definition + " [ %s ]" % self.tools['shorten_url'](url))

    return wotd
