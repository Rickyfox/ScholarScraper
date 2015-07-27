__author__ = 'Rickyfox'

import urllib2
import cookielib
from bs4 import BeautifulSoup


class ScholarScraper:



    def __init__(self):
        pass

    def getkeywordresults(self,keyword,pages):
        """
        :param keyword: keyword(s) to search google scholar for
        :param pages: number of result pages that should be processes
        :return: a list of articles that were returned from scholar for the given keyword for all pages. Articles are
                modeled as a list of their attributes (title,authors, pdfurl, year and number of citations)
        """
        results=[]
        for i in range(0,pages):
            if i is not 0:
                start=str(i)+str(0)
            else:
                start=str(i)
            l=self.searchkeyword(keyword,start)
            results+=l
        return results

    def searchkeyword(self,keyword,start):
        """
        Fetches the results from one page of the google scholar result list for the given keywords
        :param keyword: keyword(s) to search google scholar for
        :param start: result list rank at which to start, used to address different pages
        :return: a list of articles that were returned from scholar for the given keyword for one page. Articles are
                modeled as a list of their attributes (title,authors, pdfurl, year, number of citations and summary)
        """
        head='http://scholar.google.de/scholar?start='+start+'&q='
        tail='&hl=de&as_sdt=0,5'
        tsplit=keyword.split()
        query=""
        for word in tsplit:
            query+=word+'+'
        url=head+query+tail

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders.append(('Cookie', cj))
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
        response = opener.open(request)
        html = response.read()
        soup = BeautifulSoup(html)

        articles=[]
        for element in soup.find_all('div',{'class': 'gs_r'}):
            try:
                title=element.find('div',{'class' :'gs_ri'}).find('h3',{'class' :'gs_rt'}).find('a').text
                autele=element.find('div',{'class' :'gs_ri'}).find('div',{'class' :'gs_a'})
                nolinkaut=autele.text
                authors=nolinkaut.split('-')[0]
                yearstring=nolinkaut.split('-')[1]
                summary=element.find('div',{'class' :'gs_ri'}).find('div',{'class' :'gs_rs'}).text
            except:
                continue
            if ',' in yearstring:
                year=yearstring.split(',')[1]
            else:
                year=yearstring
            try:
                cites=element.find('div',{'class' :'gs_ri'}).find('div',{'class' :'gs_fl'}).findNext('a').text.split(':')[1]
            except:
                cites='0'
            pdfele=element.find('div',{'class' :'gs_ggs gs_fl'})
            if pdfele is not None:
                pdfurl=pdfele.find('div').find('a')['href']
            else:
                pdfurl=None
                #print 'no url found'
                continue

            articles.append([title,authors,pdfurl,year,cites,summary])
        return articles
