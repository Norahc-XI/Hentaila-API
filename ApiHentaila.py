import requests
from bs4 import BeautifulSoup

class ApiHentaila():
    def __init__(self, url:str) -> None:
        def categotyTags(obj:object) -> list:
            "Extraer las categorias del objeto y colocarlos en una lista | Extract the categories from the object and place them in a list"
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
        "Descargar la portada del H | Download the thumbnail of H"
        def download(url):
            "Guardar la imagen con formato .jpg | Save the image in .jpg format"
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
        "Imprime de manera ordenada la informacion basica del h | Prints in an orderly manner the basic information of the h"
        print(f"Titulo             | Title            : {self.title}")
        print(f"Tipo               | Type             : {self.type}")
        print(f"Estado             | Status           : {self.status}")
        print(f"Cantidad_Episodios | Number_Episodes  : {self.episodes}")
        print(f"Descripcion        | Description      : {self.description}")
        print(f"Categorias         | Tags             : {self.tags}")
        print(f"Puntuacion         | Punctuation      : {self.rate}")

    def watch(self) -> list:
        "Devuelve una lista con los enlaces hacia los capitulos del h | Returns a list with the links to the chapters of h"
        watchList=[]
        for i in self.PAGINA_COMPLETA.find("div", {"class":"episodes-list"}):
            try: 
                article={
                    "imgUrl":"https://hentaila.com"+i.find("img")['src'],
                    "Url":"https://hentaila.com"+i.find("a")['href']
                }
                watchList.append(article)
            except: pass
        watchList.reverse()
        return watchList

    def recommendedHs(self) -> list:
        "Devuelve una lista con diccionarios de los hentais relacionados con el h | Returns a list with dictionaries of the hentais related to the h"
        def clearInfo(article) -> dict:
            "Coloca la informacion en un diccionario | Put the information in a dictionary"
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

    def __doc__(self, lang="es"):
        "Imprime la documentacion en el idioma especificado | Print the documentation in the specified language -> Solo - Only: English / Español"
        if lang=="es":
            return ("""
                                        ---Documentacion Api de hentaila.com [NO OFICIAL]---
            Se puede acceder a toda la informacion relevante del h, simplemente usanto un punto y lo que se desea obtener.

            Opciones:
                title       : Titulo del h
                type        : Tipo del h
                status      : Estado del h
                episodes    : Cantidad de episodios
                description : Descricion del h
                tags        : categorias a las que pertenece
                thumbnail   : Url de la miniatura del h
                rate        : Puntuacion del h
            
            Ejemplos: 
                print(ApiHentaila("Url").thumbnail)
                print(ApiHentaila("Url").description)
                print(ApiHentaila("Url").status)
                print(ApiHentaila("Url").episodes)



            __init__() = Construtor, recibe la url del h, y establece las variables con su informacion.
            -
            downloadThumbnail() = Descargar la miniatura del h o de los hentais recomendados. (explicado más adelante a profundidad)
            -
            info() = Dmprime la informacion basica del h, de manera ordenada.
            -
            watch() = Devuelve una lista con diccionarios de los episodios con sus miniaturas
            -
            recommendedHs() = devuelve una lista con diccionarios sobre los h relacionados que aparecen al lado del h.
                Cada diccionario tiene tres valores: ('"imgUrl" : Url de la portada del h
                                                    "title" : El titulo del h
                                                    "Url" : Url hacia el h').

                Para acceder a cada uno de ellos se usa: Var["title"]. Ejemplo: Var = ApiHentaila().recommendedHs()[0]["title"]
            -
            __doc__() = Solo imprime esta documentacion en dos idiomas - Español y Ingles



            downloadThumbnail() Parte 2 = Se puede usar con la lista que devuelve 'recommendedHs()' para descargar las portadas de los h relacionados.
            Uso:
                ```
                1. App = ApiHentaila("URL")
                2. I = 0
                3. for art in App.recommendedHs():
                4.    print(App.downloadThumbnail(OutputPath = str(I), RHDictImg = art))
                5.    I+=1
                ```


            downloadThumbnail() Parte 3 = Tambien es posible usarlo para descargar las miniaturas de los capitulos del h.
            Uso:
                ```
                1. I = 0
                2. App = ApiHentaila("URL")
                3. for art in App.watch():
                4.     print(App.downloadThumbnail(OutputPath = str(I), RHDictImg = art))
                5.     I+=1
                ```
            """)
        elif lang=="en":
            return ("""
                                --- Api Documentation of hentaila.com [NOT OFFICIAL] ---
            You can access all the relevant information about h, simply using a point and what you want to obtain.

            Options:
                title: Title of h
                type: h type
                status: State of h
                episodes: Number of episodes
                description: Description of h
                tags: categories to which it belongs
                thumbnail: h thumbnail url
                rate: h score
            
            Examples:
                print(ApiHentaila("Url").thumbnail)
                print(ApiHentaila("Url").description)
                print(ApiHentaila("Url").status)
                print(ApiHentaila("Url").episodes)



            __init__() = Builder, receives the url of the h, and sets the variables with their information.
            -
            downloadThumbnail() = Download the thumbnail of the recommended hentai. (explained later in depth)
            -
            info() = Print the basic information of h, in an orderly way.
            -
            watch() = Returns a list with dictionaries of the episodes with their thumbnails
            -
            recommendedHs() = returns a list with dictionaries about the related h's that appear next to the h.
                Each dictionary has three values: ('"imgUrl": Url of the home page of the h
                                                    "title": The title of the h
                                                    "Url": Url towards h ').

                To access each of them, use: Var["title"]. Example: Var = ApiHentaila().RecommendedHs()[0]["title"]
            -
            __doc __ () = Only print this documentation in two languages ​​- Spanish and English



            downloadThumbnail() Part 2 = It can be used with the list that returns 'recommendedHs()' to download the covers of the related hs.
            Use:
                ```
                1. App = ApiHentaila("Url")
                2. I = 0
                3. for art in App.recommendedHs():
                4. print (App.downloadThumbnail(OutputPath = str(I), RHDictImg = art))
                5. I+=1
                ```
 

            downloadThumbnail() Part 3 = It is also possible to use it to download the miniatures of the h chapters.
            Use:
                ```
                1. I = 0
                2. App = ApiHentaila("URL")
                3. for art in App.watch():
                4. print (App.downloadThumbnail(OutputPath = str(I), RHDictImg = art))
                5. I+=1
                ```
            """)
        else:
            return "Idioma no disponible | Language not available"