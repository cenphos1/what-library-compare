"""
This is a quick script to get what I wanted done.
The code isn't pretty, I'm sure I'm doing a lot wrong.
There are plenty of bugs, I only debugged what I needed to do to make it work for me.
I'm sharing it so that someone else might be able to hack it together to work for them too.

I scraped bibliocommons search page to get the results.
Tons of libraries use bibliocommons so I think it should work.
I did a custom search in which I listed all CDs at a local library

LIMIT THE RESULTS TO 1 PER PAGE
You can set this in the url under display_quantity=1
I did a bit of testing and bibliocommons works up to 100, if you want to edit the scraping to make it work for multiple entries
"""

# Imports

import requests
from bs4 import BeautifulSoup
import sqlite3
# mad credit to isaaczafuta for writing the python implementation of the whatapi and making my life super easy https://github.com/isaaczafuta/whatapi
import whatapi.whatapi
import time

# Globals

# Set this to the number of pages you want to crawl
# For my use case this was 8500, it takes awhile
xPages = 10

# What.cd user/pass CHANGE THIS BEFORE SHARING IT
apiuser = whatapi.whatapi.WhatAPI(username='', password='')


# Set this to wherever you want your database to be.
dbConnect = sqlite3.connect('database/sqlite.db')
c = dbConnect.cursor()

# Pull data from bibliocommons    

def page_crawl(pages):
    counter = 1
    # Change the counter to the number of pages you would like to crawl before you start, yo.
    # Final will be > 8000
    while counter < pages:        
        # Pull the page from bibliocommons. This rides on a dirty url hack.
        # Copy from the search URL you get for your local library from bibliocommons, you want the page= to be on the end (to iterate over the pages) and the display_quantity to be 1
        r = requests.get('display_quantity=1&page=' + str(counter))
        content = r.content

        # Beautiful Soup

        soup = BeautifulSoup(content)
        
        # Parse it!
        found = soup.find("span", class_="title")
        try:
            title = found.next_element.next_element    
            foundArtist = soup.find("span", class_="author")
        except AttributeError:
            title = "NO TITLE PRESENT"
        try:
            artist = foundArtist.next_element.next_element.next_element
            if artist[-14:-1] == "Musical group":
                artist = artist[0:-16]
            
            # and this little hack is because bibliocommons lists an artist like "Frank Zappa" as "Zappa, Frank"
            elif "," in artist:
                artist = artist.split(",")
                artist = artist[1] + ' ' + artist[0]

            else:
                pass
        except AttributeError:
            artist = ""

        print str(counter) + "Got %s - %s" % (title, artist)
        # Inserts cd into the database, does not commit it.
        c.execute('INSERT INTO libmusic VALUES (?,?)', (title, artist))
        counter+=1

    # Now commit all dem entries
    dbConnect.commit()

    # And launch into the checking
    check_what()


# Now we check what.cd

def check_what():
    library = c.execute('SELECT title, artist FROM libmusic').fetchall()
    
    for title, artist in library:
        # unicode() because there's nothing like finding out that your script that was running all night crashed because python can't stitch an integer and string together
        search = unicode(title) + " " + unicode(artist)
        output = apiuser.request('browse', searchstr=search)
        # Delay the loop for 2 seconds. Keep within the rate limit of what.cd
        time.sleep(2)
        
        # The output that is sent back from the request if the search returns nothing.
        if output == {u'response': {u'results': [], u'youMightLike': []}, u'status': u'success'}:
            c.execute('INSERT INTO checkout VALUES (?, ?)', (title, artist))
            print "Added %s - %s" % (unicode(title), unicode(artist))
        
        else:
            pass

    dbConnect.commit()
            
        
    print "Wow, that was a lot of data! All done!"


if __name__ == '__main__':
    page_crawl(xPages)