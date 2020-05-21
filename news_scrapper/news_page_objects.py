from common import config
import requests
import bs4

class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None	
        self._visit(url)
        self._url = url

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()  #Este metodo nos permite arrojar un 
        #error si la solicitud no se hizo bien
	
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')
    

class HomePage(NewsPage):
    def __init__(self,news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)

class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def title(self):
        result = self._select(self._queries['article_title'])

        return result[0].text if len(result) else ''
   
    @property
    def body(self):
        result1 = self._select(self._queries['article_body'])
        if len(result1)>1:
            result = []
            for i in range(len(result1)-12):
                result.append(result1[i-1].text if len(result1) else '')
                
            return " ".join(result)
        elif len(result1)==1:
            return result1[0].text if len(result1) else ''
        #result = self._select(self._queries['article_body'])
        #return result[0].text if len(result1) else ''
   
    @property
    def url(self):
        return str(self._url)
 

