from flask import Flask, render_template, request
from src.gemini_api import QuestGemini
from src.source_news import News


class SiteNews:
    def __init__(self,api_key):
        '''
        Classe responsavel por gerar o site de noticias usando Flask
        E Aplicar Gemini para ajudar e resumir as buscas do Google News e BeautifulSoup
        '''
        self.flask_app = Flask(__name__)
        self.api_key = api_key

        @self.flask_app.route("/", methods=["GET", "POST"])
        def index():
            results = []
            error = None

            if request.method == "POST":
                query = request.form.get("query")
                

                if not query or not api_key:
                    error = "Por favor, insira o assunto e a API key."
                else:
                    try:
                        quest = QuestGemini(api_key, query)
                        keywords = quest.generate_keywords()

                        news_fetcher = News(keywords)
                        news_results = news_fetcher.fetch_all()

                        for item in news_results:
                            if item["text"]:
                                resumo = quest.news_summary(item["text"])
                                results.append({
                                    "tema": item["news"],
                                    "titulo": item["title"],
                                    "site": item["site"],
                                    "resumo": resumo,
                                    "url": item["url"],
                                    "data": item["date"]
                                })

                    except Exception as e:
                        error = f"Erro: {e}"

            return render_template("index.html", results=results, error=error)

    def run(self, host="0.0.0.0", port=5000, debug=True):
        self.flask_app.run(host=host, port=port, debug=debug)
