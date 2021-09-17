import requests
from bs4 import BeautifulSoup

class ApiHentaila():
    def __init__(self, url:str) -> None:
        def categotyTags(obj:object) -> list:
            "Extraer las categorias del objeto y colocarlos en una lista"
            tagged=[]; 
            for i in obj: tagged.append(i.text)
            return tagged

        self.PAGINA_COMPLETA=BeautifulSoup(requests.get(url).content, "html.parser")
        self.title:str=self.PAGINA_COMPLETA.find("h1").text
        self.type:str=self.PAGINA_COMPLETA.find_all("span")[3].text
        self.status:str=self.PAGINA_COMPLETA.find_all("span")[4].text.split()[1]
        self.episodes:int=int(self.PAGINA_COMPLETA.find_all("span")[6].text)
        self.description:str=self.PAGINA_COMPLETA.find_all("p")[1].text
        self.tags:list=categotyTags(self.PAGINA_COMPLETA.find_all("a", {"class":"btn sm"}))
        self.thumbnail:str="https://hentaila.com"+self.PAGINA_COMPLETA.find("img", {"alt":"hentai"})["src"]
        self.rate:float=float(self.PAGINA_COMPLETA.find("p", {"class":"fa-star total"}).text.split()[0])
        self.__about__:str="API de la Web Site de https://hentaila.com - Uso Libre, No me hago responsable del uso hacia esta Api @NorahcXI"

    def downloadThumbnail(self, OutputPath:str="Portada", RHDictImg:dict=None):
        def download(url):
            Img=requests.get(url)
            File=open(OutputPath+".jpg", "wb")
            File.write(Img.content)
            File.close()

        if RHDictImg!=None: 
            download(RHDictImg["imgUrl"])
        else: 
            download(self.thumbnail)

        return "Descargado | Downloaded"
    
    def info(self) -> str:
        print(f"Titulo             | Title            : {self.title}")
        print(f"Tipo               | Type             : {self.type}")
        print(f"Estado             | Status           : {self.status}")
        print(f"Cantidad_Episodios | Number_Episodes  : {self.episodes}")
        print(f"Descripcion        | Description      : {self.description}")
        print(f"Categorias         | Tags             : {self.tags}")
        print(f"Puntuacion         | Punctuation      : {self.rate}")

    def watch(self) -> list:
        watchList=[]
        for i in self.PAGINA_COMPLETA.find("div", {"class":"episodes-list"}):
            try: watchList.append("https://hentaila.com"+i.find("a")['href'])
            except: pass
        watchList.sort()
        return watchList

    def recommendedHs(self) -> list:
        def clearInfo(article) -> dict:
            dicTemp={
                "imgUrl":"https://hentaila.com"+article.find("img")["src"],
                "title":article.find("h2").text,
                "Url":"https://hentaila.com"+article.find("a")["href"]
            }
            return dicTemp

        ListHentais=[]
        contenedor=self.PAGINA_COMPLETA.find("div", {"class":"grid hentais"})
        articulos=contenedor.find_all("article")
        for i in articulos:
            ListHentais.append(clearInfo(i))
        return ListHentais

    def __doc__(self):
        return ("""Documentacion completa : Proximamente""")