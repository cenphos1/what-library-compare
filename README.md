what-library-compare
====================

Compares CDs available at local library to see if they're on what.cd

This is a quick and dirty script. You're going to have to edit a couple of things in the source code to get it to (maybe) work for you. I'm just sharing it to maybe help someone else out.

I'd recommend setting up a virtualenv to run it in.

## Dependencies

All of these are imported in

* Requests 

    pip install requests

* whatapi (already have the files in the repo) credit to [isaaczafuta](https://github.com/isaaczafuta/whatapi)
* Beautiful Soup 

    pip install beautifulsoup4

## Variables

You'll have to edit a couple of variables in whatcompare.py

Set the number of CD listing pages you'd like to crawl the default (and a good number to test on) is 10.

    29 xPages = 10

Set your what.cd username/pass

    32 apiuser = whatapi.whatapi.WhatAPI(username='yournick', password='yourpasswd')

Now set the url for your library's bibliocommons, do a custom search to get the exact url, just remember you're aiming for a results per page of 1 (edit the URL) and page= to be at the end, delete the 1 off the end of page=1.

    48  r = requests.get('bibliocommons.com/search?custom_query=formatcode%3A(MUSIC_CD+)&suppress=true&custom_edit=false&display_quantity=1&page=' + str(counter))


Now set up the database and run it, and let it do its thing for several hours. It may be best to just let it run overnight.

    sqlite3 database/sqlite.db < schema.sql
    python whatcompare.py

For me this narrowed it down from 8500 entries to around 3000, while still tons of entries it's slightly more managable and you cut out a lot of what is already on what.cd. You should still double check as lots of it will be childrens music or named differently than it is on what.cd.
