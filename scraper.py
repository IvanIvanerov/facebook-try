# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import scraperwiki
import urlparse
import simplejson
import time
import urllib2
import re

source_url = "http://graph.facebook.com/"

try:
    last_db_value = scraperwiki.sqlite.execute("select MAX(id) from swdata")
    value = str(last_db_value.values()[1])
    last_profile_id = 586155683
except:
    last_profile_id = 586155683

while True:
    time.sleep(0)
    profile_url = urlparse.urljoin(source_url, str(last_profile_id))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(profile_url))
        profile = dict()
        profile['id'] = int(results_json.get('id'))
        profile['name'] = results_json.get('name', "")
        profile['first_name'] = results_json.get('first_name', "")
        profile['last_name'] = results_json.get('last_name', "")
        profile['link'] = results_json.get('link', "")
        profile['username'] = results_json.get('username', "")
        profile['gender'] = results_json.get('gender', "")
        profile['locale'] = results_json.get('locale', "")

        scraperwiki.sqlite.save(unique_keys=['id'], data=profile)
        last_profile_id += 1
    except urllib2.HTTPError, err:
        last_profile_id += 1
        continue
        
