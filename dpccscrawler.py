from __future__ import unicode_literals
 
from google.appengine.ext import db
from datetime import datetime
import urllib2
from lxml import html

import pdb

DPCC_URL_AREA_ANAND_VIHAR = 'http://www.dpccairdata.com/dpccairdata/display/avView15MinData.php'
DPCC_URL_AREA_MANDIR_MARG = 'http://www.dpccairdata.com/dpccairdata/display/mmView15MinData.php'
DPCC_URL_AREA_PUNJABI_BAGH = 'http://www.dpccairdata.com/dpccairdata/display/pbView15MinData.php'
DPCC_URL_AREA_RK_PURAM = 'http://www.dpccairdata.com/dpccairdata/display/rkPuramView15MinData.php'
DPCC_URL_AREA_IGI_AIRPORT = 'http://www.dpccairdata.com/dpccairdata/display/airpoView15MinData.php'
DPCC_URL_AREA_CIVIL_LINES = 'http://www.dpccairdata.com/dpccairdata/display/civilLinesView15MinData.php'

DPCC_URL_ALL_AREAS = {
    'ANAND VIHAR' : DPCC_URL_AREA_ANAND_VIHAR,
    'MANDIR MARG' : DPCC_URL_AREA_MANDIR_MARG,
    'PUNJABI BAGH': DPCC_URL_AREA_PUNJABI_BAGH,
    'RK PURAM' : DPCC_URL_AREA_RK_PURAM,
    'CIVIL LINES' : DPCC_URL_AREA_CIVIL_LINES
    }

def get_datetime(dt, tm):
    dtmstring = "%s::%s" %(dt, tm)
    #dtm = datetime.strptime(dtmstring, "%A, %B %d, %Y::%H:%M:%S")
    return dtmstring

def unicode_escape(v):
    return v.encode('unicode-escape')

class DPCCItem(db.Model):
    area = db.StringProperty(required=True)
    parameter = db.StringProperty(required=True)
    date = db.StringProperty(required=True)
    value = db.StringProperty(required=True)
    standard = db.StringProperty(required=False)

    def __str__(self):
        return "Area: %s::Date: %s, Parameter: %s, Value: %s, Standard: %s" %(self.area, str(self.date), 
                str(self.parameter), unicode_escape(self.value), unicode_escape(self.standard))

class DPCCAirScrawler:
    @staticmethod
    def scrape():
        for a, area_url in DPCC_URL_ALL_AREAS.iteritems():
            try:
                response = urllib2.urlopen(area_url)
                raw_html = response.read()
                dom = html.fromstring(raw_html)
                pollution_data = dom.xpath("//tr[@class='tdcolor1']|//tr[@class='tdcolor2']")
                for pd in pollution_data:
                    pm = pd.xpath('./td[1]/text()')[0].strip()
                    dt = pd.xpath('./td[2]/text()')[0].strip()
                    tm = pd.xpath('./td[3]/text()')[0].strip()
                    vl = pd.xpath('./td[4]/text()')[0].strip()
                    ut = pd.xpath('./td[4]/text()')[0].strip()
                    st = pd.xpath('./td[5]/text()')[0].strip()

                    # Check if value has a <sup> (superscript) as well and get that
                    sup = pd.xpath('./td[4]/sup/text()')
                    
                    if sup:
                        sup = sup[0].strip()
                        vl = vl + sup
                        ut = ut + sup
                        st = st + sup

                    print "ar: %s, pm: %s, dt: %s, tm: %s, vl: %s, st: %s" % (a, str(pm), str(dt), str(tm), 
                                            unicode_escape(vl), unicode_escape(st))

                    item = DPCCItem(area=a, parameter=str(pm), value=vl, date=get_datetime(dt, tm))
                    item.standard = st
                    item.put()
            except urllib2.URLError as e:
                print "URL Open Status Code Exception: %s" % str(e)

        #retval = ''
        #for item in DPCCItem.all():
        #    retval = retval + "\n" + str(item)

        #return retval