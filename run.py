from src.main import SiteNews
filename = 'api_key.txt'
try:
    with open(filename, "r") as file:
        api_key = file.readline().strip()
except FileNotFoundError:
    print(f"Erro: O arquivo '{filename}' não foi encontrado.")
news = SiteNews(api_key = api_key)
news.run()