from google import genai

class QuestGemini:

    def __init__(self,key_api,theme):
        '''
        Classe com as funcoes que usam a IA gemini
        Args:
            key_api: Chave api do gemini
            theme (str): O assunto de interesse (ex: 'soja', 'milho', 'Corinthians').
        '''
        self.client = genai.Client(api_key= key_api)
        self.theme = theme
        self.prompt_theme = f"Crie uma lista de palavras-chave relacionadas a '{self.theme}', adequada para pesquisa no Google Notícias. A lista deve ser uma única string separada por vírgulas, sem frases adicionais."


    def generate_keywords(self):
        """
        A IA vai dar dica de uma lista de palavras-chave para pesquisa no Google Notícias.
        Returns:
            list: Uma lista de strings com as palavras-chave sugeridas.
        """
        response = self.client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents= self.prompt_theme,
                    )
        keywords_string = response.text

        # Processamento da resposta para criar a lista
        keywords_list = [keyword.strip() for keyword in keywords_string.split(',')]

        return keywords_list
    
    def news_summary(self,news_text):
            '''
            A IA vai resumir as noticias dos assuntos de interrese
            Args:
                news_text (str) : noticia completa sobre algum assunto 
            Returns: 
                Uma str que é o resumo da notícia do argumento, com no máximo 3 frases.

            '''
            prompt = f"Por favor, resuma a seguinte notícia em no máximo 3 frases, focando nos pontos mais importantes. \n\nNotícia: {news_text}"
            response = self.client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents= prompt,
                    )
            return response.text

    
