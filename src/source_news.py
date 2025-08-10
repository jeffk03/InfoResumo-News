import requests
from bs4 import BeautifulSoup
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from GoogleNews import GoogleNews
import logging

logger = logging.getLogger(__name__)

class News:
    def __init__(self, news_list, max_workers=8):
        '''
        Classe responsavel para encontrar noticias do dia de hoje usando a biblioteca de GoogleNews e extração do texto usando bs4
        O usuario fornece uma lista com os assuntos que ele quer saber as noticias 
        '''
        self.news_list = news_list
        self.day = date.today()
        self.max_workers = max_workers

    def _clean_link(self, link: str) -> str:
        return link.split('&')[0]

    def _extract_news_text(self, url: str) -> str:
        '''
        Buscar e extrair o conteúdo do texto principal de um artigo de notícias
        '''
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Error accessing URL: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()

        # Tentativa de achar <article> tag
        article = soup.find('article')
        if article:
            return article.get_text(separator="\n", strip=True)

        # concatenate todos <p> elementos
        paragraphs = soup.find_all('p')
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return text

    def _source_news(self, query: str):
        '''
        Funcao usa googlenews para encontrar noticias e um breve tratamento.
        '''
        google = GoogleNews(period='d')
        google.setlang('pt')
        google.search(query)
        results = google.results() or []

        output = []
        for r in results:
            url = self._clean_link(r.get('link', ''))
            try:
                news_text = self._extract_news_text(url)
            except Exception as e:
                #logger.exception("Error extracting news from %s: %s", url, e) # Mostra noticias onde o scrapy n deu boa 
                news_text = None

            output.append({
                'news': query,
                'title': r.get('title'),
                'site': r.get('media'),
                'text': news_text,
                'url': url,
                'date': self.day,
                'desc': r.get('desc')
            })
        return output

    def fetch_all(self, timeout_per_task=None):
        '''
        Busca todas as noticias da lista fornecida pelo usuario usando Paralelismo
        '''
        all_results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_query = {executor.submit(self._source_news, q): q for q in self.news_list}
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    res = future.result(timeout=timeout_per_task)
                    all_results.extend(res)
                except Exception as e:
                    logger.exception("Failed to process query '%s': %s", query, e)
        return all_results


# Example usage:
# news_obj = News(["soja", "sal", "cofe"], max_workers=10)
# results = news_obj.fetch_all()
# print(results)
