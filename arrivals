#!/usr/bin/env python3
# arrivals.py - Fetch and print all arrivals/depertures given an IATA airport code  
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Author:      E:V:A
#  Date:        2018-01-08
#  Last:        2022-01-21
#  Repo/Bugs:   https://github.com/E3V3A/IataArrivals
#  Version:     1.0.2   (pyflightdata-0.8.5)
#  Codec:       utf_8
#  License:     GPLv3
#  Donate?      BTC:    
#               
#----------------------------------------------------------------------------
# 
#  Description:
#   
#    A simple python app to primarily display current arrivals and departures, given 
#    an airports' IATA code (3 letters). However, it can also list all API available 
#    airports given a country name or airport details given an IATA code, and more.. 
#  
#  Required Installation:
# 
#    git clone https://github.com/supercoderz/pyflightdata.git
#    pip install pyflightdata
# 
#  Run with:
#
#    ./arrivals.py <airport-IATA-code>
# 
#  Debug with:
#
#   (a)    ./arrivals.py -j 1 CPH | json_pp -f json -t dumper -json_opt pretty,utf8,allow_singlequote
#                                 | python -m json.tool | pygmentize -g
#           python -c "from pyflightdata import FlightData as fd; a=fd().get_flights_from_to('OSL','TLV'); print(a);"
#
#   (b)  Directly in python CLI:
#           from pyflightdata import FlightData as fd
#           da = fd().get_airport_arrivals("KAL")
#           print (da)
#
#   (c) To update (repo) installed pyflightsdata you may need to do: 
#       pip install --ignore-requires-python --ignore-installed --force-reinstall -e .
#
#  =============================   WARNING!  ================================
# 
#  * This app could easily break and most probably will eventially, because 
#    it's functionality depends on several external sites and the tools used 
#    to scrape those sites. Also you risk to get your IP banned from using 
#    those sites and/or their API services in case of misuse by multiple
#    and rapid requests. Please respect the providers of free services!
# 
#  * Do not use the METAR from this app for professional use, it's probably 
#    not as up-to-date as that provided by other sources/services. 
# 
#----------------------------------------------------------------------------
# 
#  Other API sources/info:
# 
#       [1] http://pyflightdata.readthedocs.io/en/latest/pyflightdata.html
#       [2] https://www.latlong.net/
#       [3] https://aviationweather.gov/
#       [4] http://services.faa.gov/airport/status/<IATA_CODE>?format=application/json
#       [5] http://www.fly.faa.gov/flyfaa/usmap.jsp
#       [6] https://www.radarbox24.com/
#       [7] https://opensky-network.org/
# 
#  Other sources we could support:
# 
#       [ ] OpenSky-Network:
#           URL:    https://github.com/openskynetwork/opensky-api
# 
#       [ ] FlightRadar24:
#           URL:    https://github.com/mkorkmaz/flightradar24/
#           URL:    https://api.flightradar24.com/common/v1/airport.json?code=ist&plugin[]=&plugin-setting[schedule][mode]=&plugin-setting[schedule][timestamp]=1515197092&page=1&limit=100&token=  
#                   under:  ['result']['response']['airport']['pluginData']['schedule']
# 
#       [ ] AviationWeather:    
#           See:    https://github.com/dam3313/MMM-aviationwx/
#           URL:    https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=EYVI&hoursBeforeNow=1
#           URL:    https://aviationweather.gov/taf/data?ids=" + icao + "&format=decoded&metars=on&layout=on
#           URL:    https://aviationweather.gov/gis/scripts/MetarJSON.php?density=all&bbox=-180,-90,180,90 
#  
#       [ ] Radarbox
#           URL:    https://www.radarbox24.com/
# 
#  Dependencies:
#       
#       - Python3               -- SELF:  datetime, getopt, json, re, sys
#       - pyflightdata          -- API:   requests, lxml, beautifulsoup4, pytest, pytest-cov, pytest-repeat, jsonpath-rw, flaky, twine, sphinx, sphinx-autobuild, sphinx_rtd_theme
#       - flightradar24         -- API:   pytest, requests, python-coveralls, coverage
#       - "others"              -- ???:   ply, decorator, html5lib, webencodings
# 
#  ToDo:    
# 
#       [ ] Fix "-i" for unknown IATA code
#       [ ] Investigate how to implement ICAO -- 4 letter airpiort codes
#       [ ] Fix sorting of JSON response so that time of arrivals/departure are in order
#       [ ] Fix "-j" CLI flag for debug mode
#       [/] Fix tabulation by using {} formatting instead of all in-string TAB's
#       [ ] Fix color check also for:  xterm-color and xterm-256color etc.
#       [ ] Add "-a" CLI flag to add API credentials by supplying a registered email and password
#       [ ] Add "-f" CLI flag for current in-flight plane information given a Flight number or Flight ID. 
#       [ ] Add "-t" CLI flag for times used for API vs. local airport TZ
#       [ ] Add alternative source(s) for other airports not available 
#       [ ] Add gate number to Departures
#       [ ] Add "-r" CLI flag to get Flightradar24 current flights within boundary box, 
#           given a [lat/lon] (decimal degrees) and radius in km. I.e.:
#           arrivals -r <lat,lon> <radius[km]> 
#           See:    1. [MMM-FlightsAbove](https://github.com/E3V3A/MMM-FlightsAbove) 
#                   2. [flightradar24-client](https://github.com/derhuerst/flightradar24-client)
#       [-] Add RealFeel temperature calulation from realfeel.py
#       [ ] ^^^ We use FeelsLike (from meteocalc) instead as RealFeel is too complicated and poorly documented.
#           https://github.com/malexer/meteocalc
#       [ ] 2022-01-20 dependencies:    ply, decorator, html5lib, webencodings, 
#       
#       
#  Dev Notes:  
#
#       - Python dictionaries are not ordered, so the key-value pairs may appear in a different order when printed
#       - All CLI arguments are strings so we need to convert all numbers to int() 
#
#----------------------------------------------------------------------------
#  Example:       <none>
# 
#----------------------------------------------------------------------------
import datetime, getopt, json, re, sys
from pyflightdata import FlightData
from metar import Metar

#------------------------------------------------
#  Variables
#------------------------------------------------
version = "1.0.2"
apicreds = 0

#------------------------------------------------
# Some text highlights
#------------------------------------------------
# Usage:  print (yellow("This is yellow"))
def color(text, color_code):
    # Potential windows issue: see issue #2
    #if sys.platform == "win32" and os.getenv("TERM") != "xterm":    # or xterm-color or xterm-256color
    #    return text
    return '\x1b[{}m{}\x1b[0m'.format(color_code, text)

def red(text): return color(text, 31);
def green(text): return color(text, 32);
#def orange(text): return color(text, 31); # Hard to look good! (or remains "red")
def yellow(text): return color(text, 33)
def blue(text): return color(text, 34)
def purple(text): return color(text, 35)
def cyan(text): return color(text, 36)
def gray(text): return color(text, 37);

#------------------------------------------------
#  Functions
#------------------------------------------------
def usage() : 
    print ("\n Usage:  arrivals.py [options] <airport-IATA-code>\n")
    print (" Options:")
#    print ("        -a <email> <passwd>  -- Use your API credentials by supplying a registered email and password")
    print ("        -d <airport-iata>    -- Show Departures instead of Arrivals (default)")
    print ("        -n <n>               -- Only show <n> number of flights")
    print ("        -i <airport-iata>    -- Show detailed information about an airport given its IATA code")
    print ("        -j <1,2>             -- Enable debug mode at level 1 or 2 to print the full JSON response")
    print ("        -l <country-name>    -- List all available airport IATA codes for a country given by <country-name>")
    print ("        -m <airport-iata>    -- Get last hour's METAR data for an airport given by its IATA <airport-code>")
#    print ("                                (This option is getting raw METAR info from:  aviationweather.gov )")
#    print ("        -f <flight/id>       -- Get in-air information (speed,alt,bearing etc) given a certain flight number or id")
#    print ("        -r <lat,lon> <radius> -- Show flights/airplanes within the given radius [km] of a decimal lat/lon location.")
#    print ("        -t                   -- Show arrival/departure times in the local timezone (TZ) of the airport")
#    print ("        -w                   -- Show the weather for the Airport given by its <iata> code")
    print ("        -x <iata-1> <iata-2> -- Show direct fligths between 2 airports given by their <iata> codes")
    print ("        -c                   -- Print Copyright License and maintenance URL.")
    print ("        -v                   -- Print program Version")
    print ("        -h, --help           -- Print this help")
    print ("\n")
    print (red(" --- IMPORTANT! -----------------------------------------------"))
    print ("   \u2022 All times shown are in the timezone of your computer!")
    print ("   \u2022 Do not attempt to run these queries in rapid succession,") 
    print ("     as your IP might get blocked by the API providers.")
    print (red(" --------------------------------------------------------------"))

# Return HH:MM:SS from Unix Time Epoch
def hs(apiTime):
    if apiTime != "None" :      # isinstance(apiTime, int) :
        tt = datetime.datetime.fromtimestamp(int(apiTime))
        tf = tt.strftime('%H:%M')
        return tf
    else :
        return "-"

# Return MM-DD HH:MM:SS from Unix Time Epoch
def hd(apiTime):
    if apiTime != "None" :      # isinstance(apiTime, int) :
        tt = datetime.datetime.fromtimestamp(int(apiTime))
        tf = tt.strftime('%Y-%m-%d %H:%M')
        return tf
    else :
        return "-"


def tz(apiTZ): 
        ##tt = datetime.datetime.fromtimestamp(int(apiTZ))
        ##tf = tt.strftime('%H:%M')
        #tz =  "UTC%+.2d" % round( int(apiTZ)/3600 )    # GMT+X = apiTZ / [seconds/hour]
        if int(apiTZ) < 0 : 
            pm = "-" 
        else : 
            pm = "+"
        secs = abs(int(apiTZ))
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        tz = ("UTC%s%02d%02d" % (pm, h, m))
        return tz

def typerr():
    print ("Unknown TypeError! Check the API code and/or JSON response.")
    return

def iataerr():
    print ("Airport IATA code not found! Check your spelling!")
    print ("NOTE: Airports need international network services to be found.")
    sys.exit()

def airerr():
    print ("Country not found! Check your spelling!") 
    print ("NOTE: Use double quotes for multi-word names and try one of:")
    print ("      https://www.listofcountriesoftheworld.com/")
    sys.exit()

def airerr2():
    #print ("Ambigous country name!")
    print ("\nUnited What? You can also use: US,USA,UK,UAE")
    sys.exit()

def copyright():
    print ("\nProgram License:  GPLv3\nMaintenance URL:  https://github.com/E3V3A/iata-arrivals-cli") 
    sys.exit()

#------------------------------------------------
#  CLI Options & Arguments
#------------------------------------------------
#def main():

badbug = False   # Enable to check CLI arguments
#badbug = True   # Enable to check CLI arguments
debug = 0
query = 1
airport = ''
airport2 = ''
country = ''
nmax = 0

try:
    opts, args = getopt.getopt(sys.argv[1:], ":chvd:i:j:l:m:n:x:", ["help", "version"])
except getopt.GetoptError :
    #print str(err)
    usage()
    sys.exit(2)

if badbug :
    print ("opts: ", opts)
    print ("args: ", args)

if not opts : 
    if not args : usage(); sys.exit();
    airport = args[0]
    query = 1                                           # Show Arrivals
else :
    for opt, arg in opts:
        if badbug :
            print ("opt: ", opt)
            print ("arg: ", arg)
        if opt in ("-h", "--help"): usage(); sys.exit();
        elif opt in ("-v", "--version"): print ("Version: ", version); sys.exit();
        #elif opt == "-a":                                      # Use API credentials
        #    apicreds = 1; apiuser = args[0]; apipass = args[1];
        elif opt == "-c": copyright();                          # Show Copyright info
        elif opt == "-d": query = 2; airport = arg;             # Show Departures from <iata>
        elif opt == "-i": query = 4; airport = arg;             # Show airport INFO from <iata>
        elif opt == "-j": debug = int(arg);                     # FIX:  airport = args[0]; country = args[0];
        elif opt == "-l": query = 3; country = arg;             # Show list of <iata> codes from <country>
        elif opt == "-m": query = 5; airport = arg.upper();     # Show last hour's METAR data for an airport given by <airport-code>
        elif opt == "-n": nmax = int(arg); #airport = args[0]                     # FIX:  Maximum number of output items/pages
        #elif opt == "-t": loctz = True;                        # Show all results in local airport TimeZone
        elif opt == "-x":                                       # Show flights between 2 airports <iata-1> <iata-2>
           query = 6; airport = arg; airport2 = args[0].upper();

if not airport and not country : airport = args[0];


# Fix for some ambigous country names ("United" for UK,US,USA,UAE)
if not country == '' :
    if country == "US" or country == "USA" :
        country = "United States"
    elif country == "UK" :
        country = "United Kingdom"
    elif country == "UAE" :
        country = "United Arab Emirates"
    elif country == "United" :
        airerr2()

if badbug :
    print ("airport: ", airport)
    print ("airport2: ", airport2)
    print ("country: ", country)
    print ("debug: ", debug)
    print ("query: ", query)
    print ("")
    #sys.exit()

#if __name__ == "__main__":
#   main()

#------------------------------------------------
#  MAIN
#------------------------------------------------

# If using API credentials
if apicreds == 1 :
    apiuser = "your-api-email@what.not"
    apipass = "your-api-password"
    api=FlightData(apiuser,apipass)
    api.login(apiuser,apipass)
    # Don't forget to: api.logout()
else :
    api=FlightData()    # Skip API credentials


if query == 1 : 
    if nmax == 0:
        alist = api.get_airport_arrivals(airport);    # Return: a JSON dictionary of xxxxx 
    else :
        alist = api.get_airport_arrivals(airport, page=1, limit=nmax); 
    if not alist : iataerr();
elif query == 2 : 
    if nmax == 0 :
        alist = api.get_airport_departures(airport);  # Return: a JSON dictionary of xxxxx
    else :
        alist = api.get_airport_departures(airport, page=1, limit=nmax);
    if not alist : iataerr();
elif query == 3 : 
    try: 
        alist = api.get_airports(country);            # Return: a list of (name,code) tuples. # api.get_airports('India')[10:15]
    except AttributeError :
        airerr();
    if not alist : airerr();
elif query == 4 : 
    try: 
        alist = api.get_airport_details(airport);     # Return: 
        blist = api.get_airport_weather(airport);     # Return: 
    except AttributeError :
        iataerr();
    except TypeError :
        typerr(); iataerr();
    if not alist or not blist : iataerr();
elif query == 5 : 
    try: 
        blist = api.get_airport_weather(airport);     # Return: 
    except AttributeError :
        iataerr();
    except TypeError :
        typerr(); iataerr();
    if not blist : iataerr();
elif query == 6 : 
    try: 
        alist = api.get_flights_from_to(airport, airport2);  # Return: a JSON dictionary of xxxxx
    except AttributeError :
        Print('Attribute exception'); #airerr();
    if not alist : 
        print('empty list - no conncting flights?'); airerr();


if apicreds == 1 : api.logout();

if debug == 1 : 
    print ("Debug List: ")
    print ("\n", (alist)[0], "\n\n")
    if badbug :
        sys.exit()
if debug == 2 : 
    print (alist)
# if debug == "3" : 
#     for flight in (alist)[0] :
#         for key, value in flight.iteritems():
#             print key, 'is:', value
#         print ''


#------------------------------------------------
#  ARRIVALS
#------------------------------------------------
if query == 1 : 

    #HLine = ("ID\t Flight\t From\t Sched\t ETA\t Airline\t Status") #  callsig, flight1, origin, hs(timeS), hs(timeE), airlinN, status
    HLine = ("ID\t Flight\t From\t Sched\t ETA\t %s\t %s"% ("Airline".ljust(24,' '), "Status".ljust(15,' ')) )
    Hleng = len(HLine) + 6*4  # also count 4-space tab lengths 

    print ("\nNOTE: All times shown are in the timezone of the script!\n")
    print ("%s ARRIVALS:"% (airport) )
    print ("-"*Hleng)
    print (HLine)
    print ("-"*Hleng)

    for aL in alist:
        status  = aL['flight']['status']['text']                                # "Estimated 15:09"
        
        # Sometime destinations doesn't have an IATA code or is unknown
        if aL['flight']['airport']['origin'] == "None" :
            origin = "---"
        else :
            origin  = aL['flight']['airport']['origin']['code']['iata']         # WAW
        
        callsig = aL['flight']['identification']['callsign']                    # LOT779
        flight1 = aL['flight']['identification']['number']['default']           # LO779
        #flight2 = aL['flight']['identification']['number']['alternative']       # EE779
        #airlinI = aL['flight']['airline']['code']['icao']                       # EST

        if aL['flight']['airline'] == "None" :
            airlinN = "---"
        else :
            airlinN = aL['flight']['airline']['name']                           # Nordica
        
        timeS   = aL['flight']['time']['scheduled']['arrival']                  # 1515331200 
        timeE   = aL['flight']['time']['estimated']['arrival']                  # 1515330560 
        #timeR   = aL['flight']['time']['real']['arrival']                       # None 
        #timeO   = aL['flight']['time']['other']['eta']                          # 1515330560 
        #TZO     = aL['flight']['airport']['destination']['timezone']['offset']  # 7200 [seconds]

        if status == "Scheduled" : status = "-"
        if re.match( r'[Dd]elayed', status ) : status = yellow(status);
        if re.match( r'[Cc]anceled', status ) : status = red(status);
        if re.match( r'[Ll]anded', status ) : status = green(status);
        airline = airlinN[:24].ljust(24,' ')

        #FLine = ("%s\t %s\t %s\t %s\t %s\t %s\t %s"% (callsig, flight1, origin, hs(timeS), hs(timeE), airline, status) )
        FLine = ("{}\t {}\t {}\t {}\t {}\t {}\t {}".format(callsig, flight1, origin, hs(timeS), hs(timeE), airline, status) )
        print (FLine)

#------------------------------------------------
#  DEPARTURES
#------------------------------------------------
if query == 2 : 

    #HLine = ("ID\t Flight\t From\t Sched\t ETA\t Airline\t Status") #  callsig, flight1, origin, hs(timeS), hs(timeE), airlinN, status
    HLine = ("ID\t Flight\t To\t Sched\t ETA\t %s\t %s"% ("Airline".ljust(24,' '), "Status".ljust(15,' ')) )
    Hleng = len(HLine) + 6*4  # also count 4-space tab lengths 

    print ("\nNOTE: All times shown are in the timezone of the script!\n")
    print ("%s DEPARTURES:"% (airport) )
    print ("-"*Hleng)
    print (HLine)
    print ("-"*Hleng)

    for aL in alist:
        callsig = aL['flight']['identification']['callsign']                    # LOT779
        flight1 = aL['flight']['identification']['number']['default']           # LO779
        #flight2 = aL['flight']['identification']['number']['alternative']      # EE779
        #dgate = aL['flight']['airport']['origin']['info']['gate']               # B19
        
        # Sometime destinations doesn't have an IATA code or is unknown
        if aL['flight']['airport']['destination'] == "None" :
            goingto = "---"
        else :
            goingto = aL['flight']['airport']['destination']['code']['iata']    # WAW

        timeS   = aL['flight']['time']['scheduled']['departure']                # 1515331200 
        timeE   = aL['flight']['time']['estimated']['departure']                # 1515330560 
        #timeR   = aL['flight']['time']['real']['departure']                    # None 
        #timeO   = aL['flight']['time']['other']['eta']                         # 1515330560 
        
        if aL['flight']['airline'] == "None" :
            airlinN = "---"
        else :
            airlinN = aL['flight']['airline']['name']                           # Nordica
        
        #airlinI = aL['flight']['airline']['code']['icao']                      # EST
        status  = aL['flight']['status']['text']                                # "scheduled"
        #TZO     = aL['flight']['airport']['destination']['timezone']['offset'] # 7200 [seconds]

        if status == "Scheduled" : status = "-"
        if re.match( r'[Dd]elayed', status ) : status = yellow(status);
        if re.match( r'[Cc]anceled', status ) : status = red(status);
        #re.sub( r'([Dd]elayed)', yellow(group(1)), status, 1)
        airline = airlinN[:24].ljust(24,' ')

        FLine = ("%s\t %s\t %s\t %s\t %s\t %s\t %s"% (callsig, flight1, goingto, hs(timeS), hs(timeE), airline, status) )
        print (FLine)

#------------------------------------------------
#  AIRPORTS  "-l <country>"
#------------------------------------------------
if query == 3 : 

    HLine = ("IATA\t %s"% ("Airport Name".ljust(50,' ')) )
    Hleng = len(HLine) + 4

    print ("\nAIRPORTS in %s"% (country) )
    print ("-"*Hleng)
    print (HLine)
    print ("-"*Hleng)
    
    for aL in alist:
        iata = aL['iata']
        name = aL['name'][:50].ljust(50,' ')

        FLine = ("%s\t %s"% (iata, name) )
        print (FLine)

#------------------------------------------------
#  AIPORT INFO  "-i <iata>"
#------------------------------------------------
if query == 4 : 

    # We want: 
    # ICAO, Lat, Lon, Elev, TimeZone, ArrDelayIdx, DepDelayIdx, Country (code), City, Name, URL 
    #HLine = ("IATA\t %s"% ("Airport Name".ljust(50,' ')) )
    # Dummy line to get approximate measure
    HLine = ("(Lat,Lon) [degrees]:\t%s," % "anything".ljust(50,' ')) 
    Hleng = len(HLine) + 4

    print ("\nAIRPORT INFO for %s"% (airport) )
    print ("-"*Hleng)
    #print (HLine)
    #print ("-"*Hleng)
    
    #for aL in alist:
    aL = alist
    bL = blist
    if True :
        icao  = aL['code']['icao']
        name  = aL['name'][:50].ljust(50,' ')

        lat   = aL['position']['latitude']
        lon   = aL['position']['longitude']
        #elev  = aL['position']['elevation']    # Using: get_airport_details() // This one returns only in [feet] 
        elev  = bL['elevation']['m']            # Using: get_airport_weather() // [m], [ft]

        count = aL['position']['country']['name']
        ccode = aL['position']['country']['code']
        city  = aL['position']['region']['city']

        TZN   = aL['timezone']['name']
        TZA   = aL['timezone']['abbr']
        TZO   = aL['timezone']['offset']
        TZD   = aL['timezone']['isDst']

        Adeli = aL['delayIndex']['arrivals']
        Ddeli = aL['delayIndex']['departures']

        url = aL['url']['homepage']

        #--------------------------------------------------
        # Weather Info
        #--------------------------------------------------
        iflight = bL['flight']['category']
        metar   = bL['metar']
        skycond = bL['sky']['condition']['text']

        # Fix for API bug that can return "None" and sometimes unreasonable number for [km]
        # d * 1.609344; // convert (Statue Miles) SM to Kilometers
        visi_unit = "km"
        skyvisi = bL['sky']['visibility']['km']
        if skyvisi == "None" :
            skyvisi = "-" 
        elif int(skyvisi) > 100000 :
            skyvisi = bL['sky']['visibility']['nmi']
            visi_unit = "nmi"
        
        skytime = bL['time']

        windspd = bL['wind']['speed']['kmh']
        winddeg = bL['wind']['direction']['degree']
        winddir = bL['wind']['direction']['text']
        
        tempc = bL['temp']['celsius']
        tempd = bL['dewpoint']['celsius']
        press = bL['pressure']['hpa']
        humid = bL['humidity']


        #FLine = ("%s\t %s"% (iata, name) )
        print ("Name:\t\t\t%s" % ( yellow(name)) )
        print ("ICAO:\t\t\t%s" % (icao) )
        print ("(Lat,Lon) [degrees]:\t%s,%s" % (lat,lon) )

        #lalo = "%s,%s" % (lat,lon)
        #gmurl = "https://maps.google.com/?q=%s&z=12" % (lalo)
        #print ("GMaps URL:\t%s" % (gmurl) ) 
        llurl = "https://www.latlong.net/c/?lat=%s&long=%s" % (lat,lon)
        print ("Map URL:\t\t%s" % (llurl) )

        print ("Elevation [meters]:\t%s" % (elev) )
        print ("Country (code):\t\t%s (%s)" % (count,ccode) )
        print ("City:\t\t\t%s" % (city) )
        # 
        print ("Delay Index Arrivals:\t%s" % Adeli)
        print ("Delay Index Departures:\t%s" % Ddeli)
        #
        TZO = tz(TZO)
        #print ("Local Time:\t%s" % (TZO) )
        print ("TimeZone [name]:\t%s" % (TZN) )
        print ("TimeZone [short]:\t%s" % (TZA) )
        print ("TimeZone [offset]:\t%s" % (TZO) )
        print ("Daylight Saving Time:\t%s" % (TZD) )
        #
        print ("Airport URL:\t\t%s" % (url) )
        #print ("TimeZone [UTC]:\t%s" % (TZO) )
        #print (Adata)

        #--------------------------------------------------
        # Weather Info
        #--------------------------------------------------
        print ("-"*Hleng)
        print ("Weather Report @ %s" % (hs(skytime) ) )
        print ("-"*Hleng)
        
        print ("METAR:\t%s" % (green(metar)) )
        print ("Nav Category:\t\t%s" % (iflight) )
        print ("Sky Condition:\t\t%s" % (skycond) )
        print ('Visibility [{}]:\t{}'.format(visi_unit, round(skyvisi,1)) )  # Need to truncate decimals 
        print ("Wind:\t\t\t%s [km/h] %s (%s\xb0)" % (yellow(windspd), winddir, winddeg) )
        print ("Temperature [\xb0C]:\t%s" % (tempc) )
        print ("Dew Point [\xb0C]:\t\t%s" % (tempd) )
        print ("Pressure [mbar=hPa]:\t%s" % (press) )
        print ("Humidity [%%]:\t\t%s" % (humid) )

#------------------------------------------------
#  METAR  "-m <airport-iata>"
#------------------------------------------------
if query == 5 : 

    metar = blist['metar']
    obs = Metar.Metar(metar)
    
    #HLine = ('{:8>} {}'.format(airport, '(Work in progress!)') )
    Hleng = 80 # len(HLine)

    print ('\nMETAR INFO for {}'.format(yellow(airport)) )
    print ("-"*Hleng)
    #print (HLine)
    #print ("-"*Hleng)
    
    
    #for k, v in obs:
    #   print('{:20>} {}'.format(k,v))
    print(obs.string())

#------------------------------------------------
#  Direct flights from A to B
#------------------------------------------------
# python ./arrivals.py -x OSL IST
#------------------------------------------------
# We don't use ['flight'] here.
#   get_flights_from_to()
#   self._fr24.get_airline_flight_data(url, by_airports=True)
#   https://api.flightradar24.com/common/v1/search.json?query=default&origin=OSL&destination=AGP
#------------------------------------------------

if query == 6 : 

    headers = ('ID', 'Flight', 'Scheduled', 'ETD', 'Airline', 'Aircraft', 'Status')
    HLine   = ('{:<8}  {:<8} {:<16}  {:<5}  {:<24} {:<20} {:<19}'.format(*headers) ) # * = unpack the tuple
    Hleng = len(HLine) #+ 6*4  # also count 4-space tab lengths 

    print ('\nNOTE: All times shown are in the timezone of the script!\n')
    print ('DEPARTURES from {} to {}'.format(yellow(airport), yellow(airport2)) )
    print ('-'*Hleng)
    print (HLine)
    print ('-'*Hleng)

    for aL in alist:
        
        callsig = aL['identification']['callsign']                      # LOT779
        flight1 = aL['identification']['number']['default']             # LO779
        
        if ( aL['aircraft'] == 'None' ):
            aircraft = "---"
        else:
            aircraft = aL['aircraft']['model']['text']
        
        if aL['airport']['destination'] == "None" :                     # Some destinations doesn't have an IATA code or is unknown
            goingto = "---"
        else :
            goingto = aL['airport']['destination']['code']['iata']      # WAW

        timeS   = aL['time']['scheduled']['departure']                  # 1515331200 
        timeE   = aL['time']['estimated']['departure']                  # 1515330560 
        #timeR   = aL['flight']['time']['real']['departure']            # None 
        #timeO   = aL['flight']['time']['other']['eta']                 # 1515330560 
        
        if aL['airline'] == "None" :
            airlinN = "---"
        else :
            airlinN = aL['airline']['name']                             # Nordica
        #if aL['airline']['name'] = 'None' :                            # If we can't find airline name, maybe ICAO name? 
            #airlinI = aL['airline']['code']['icao']                    # EST
        
        status  = aL['status']['text']                                  # "scheduled"
        
        #TZO = aL['flight']['airport']['destination']['timezone']['offset'] # 7200 [seconds]
        
        #--------------------------------------------------
        # Truncate items that are often too long
        #--------------------------------------------------
        airline = airlinN[:24]                                          # Truncate Airline name
        aircraft = aircraft[:20]                                        # truncate
        status = status[:19]                                            # Truncate
        
        #--------------------------------------------------
        # Colorize Sttatus
        #--------------------------------------------------
        # WARNING: Do not truncate colored status, as it will break ansi coloring!
        if status == "Scheduled" : status = "-"
        #if status == "Estimated" : status = "-"
        #if "Estimated dep" in status : status = "-"
        if re.match( r'[Dd]elayed', status ) : status = yellow(status);
        if re.match( r'[Cc]anceled', status ) : status = red(status);
        if re.match( r'[Ll]anded', status ) : status = green(status);
        #re.sub( r'([Dd]elayed)', yellow(group(1)), status, 1)

        #headers = ('ID', 'Flight', 'Scheduled', 'ETD', 'Airline', 'Aircraft', 'Status')
        FLine   = ('{:<8}  {:<8} {:<16}  {:<5}  {:<24} {:<20} {:<19}'.format(callsig, flight1, hd(timeS), hs(timeE), airline, aircraft, status) ) # changed from hs() to hd()

        print (FLine)


#------------------------------------------------
#  END
#------------------------------------------------
print ("-"*Hleng)
print ("\nDone!\n")
