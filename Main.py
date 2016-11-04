import urllib.request
import re
import os
import json
import lxml.etree as ET
from datetime import *
import math
import csv
from bs4 import BeautifulSoup


def formatear(texto=""):
    def claveAValor(m):

        if m[0] == "<" and m[len(m) - 1] == ">":
            return ""

        if m in dicc:

            return dicc[m]

        return "FALTA VALOR " + m

    dicc = {}
    for i in range(65, 91):

        dicc[chr(i)] = chr(i + 32)

    dicc[r'\xc3\xa1'] = "a"
    dicc[r'\xc3\x81'] = "a"
    dicc[r'\xc3\xa9'] = "e"
    dicc[r'\xc3\x89'] = "e"
    dicc[r'\xc3\xad'] = "i"
    dicc[r'\xc3\x8d'] = "i"
    dicc[r'\xc3\xb3'] = "o"
    dicc[r'\xc3\x93'] = "o"
    dicc[r'\xc3\xba'] = "u"
    dicc[r'\xc3\x9a'] = "u"

    dicc[r'\xc3\xb1'] = "n"
    dicc[r'\xc2\xa1'] = ""

    dicc[r'\\u2026'] = "o"

    dicc[r'\xf1'] = "n"
    dicc[r'\xd1'] = "n"

    dicc[r'\xe1'] = "a"
    dicc[r'\xe9'] = "e"
    dicc[r'\xc9'] = "e"
    dicc[r'\xed'] = "i"
    dicc[r'\xcd'] = "i"
    dicc[r'\xf3'] = "o"
    dicc[r'\xf2'] = "o"
    dicc[r'\xfa'] = "u"

    vacios = [r'\n',r'\r',r'\t',r'  ',r'!',r'(',r')',r'\'',r'.',r',',r':',r';',r'|',r'"',r'=',r'&',r"'"]

    for item in vacios:
        dicc[item] = ""

    return re.sub(r'\\x\w\w\\x\w\w|\\U\w{8}|\\u\w{4}|\\x\w\w|\\n|\\t|\\r|\'|\.|\"|\,|\:|\;|\||\@\w+(?=\W)|\#\w+(?=\W)|https?\S+(?=\W)|[A-Z]|\s\s|\!|\(|\)|\<\/?(\w|\s)*\>|\=|\&', lambda m: claveAValor(m.group(0)), texto)


def cargarRSS(RSS):
    dict = {}
    if os.path.exists(RSS):
        with open(RSS, "r") as RSS:
            dict = json.load(RSS)
    return dict


def ponderar(historial, palabras):
    total = 0
    paginas = 0
    for fecha in historial:
        total += len(historial[fecha])
    resultados = {}
    for fecha in historial:
        if(fecha not in resultados):
            resultados[fecha] = {}
        for titulo in historial[fecha]:
            with urllib.request.urlopen(urllib.request.Request(historial[fecha][titulo])) as url:
                noticia = formatear(ascii(BeautifulSoup(url.read(),"html.parser").find_all("p")))
            for palabra in palabras:
                tam = len(noticia)
                frec = noticia.count(palabra) + titulo.count(palabra) * 2
                if(palabra not in resultados[fecha]):
                    resultados[fecha][palabra] = math.log(tam) * frec
                else:
                    resultados[fecha][palabra] += math.log(tam) * frec
            paginas += 1
            print(100 * paginas / total, "%")

    return resultados


def exportar(resultados):
    fechas = []
    for fecha in resultados:
        fechas.append(fecha)
    fechas.sort()
    archivo = str(datetime.now().date()) + ".txt"
    with open(archivo,"w") as f:
        writer = csv.writer(f)
        for fecha in fechas:
            for palabra in resultados[fecha]:
                row = (fecha,palabra,resultados[fecha][palabra])
                writer.writerow(row)
    print("Se exporto correctamente a " + archivo)
        


def main():
    historial = {}

    forma = {}
    forma["RSS"] = {}
    forma["RSS"]["Items"] = "//item"
    forma["RSS"]["Titulo"] = "./title"
    forma["RSS"]["Fecha"] = "./pubDate"
    forma["RSS"]["Link"] = "./link"
    RSS = cargarRSS("RSS-.py")
    print("Recolectando..")
    for diario in RSS:
        RSSitems = forma[RSS[diario]["Tipo"]]["Items"]
        RSStitulo = forma[RSS[diario]["Tipo"]]["Titulo"]
        RSSfecha = forma[RSS[diario]["Tipo"]]["Fecha"]
        RSSlink = forma[RSS[diario]["Tipo"]]["Link"]
        for seccion in RSS[diario]["Secciones"]:
            with urllib.request.urlopen(urllib.request.Request(RSS[diario]["Secciones"][seccion])) as url:
                tree = ET.parse(url)
                noticias = tree.xpath(RSSitems)
                for noticia in noticias:
                    # print(ET.tostring(noticia, encoding='utf8',
                    # method='xml'))
                    fecha = datetime.strptime(noticia.find(RSSfecha).text,
                                              "%a, %d %b %Y %H:%M:%S %z").date()
                    titulo = ascii(noticia.find(RSStitulo).text)
                    link = noticia.find(RSSlink).text
                    if(fecha not in historial):
                        historial[fecha] = {}
                    if(titulo not in historial[fecha]):
                        historial[fecha][titulo] = link
    with open("Palabras.txt", "r") as f:
        palabras = f.read().split("\n")
    print(palabras)
    print("Ponderando..")
    resultados = ponderar(historial, palabras)

    exportar(resultados)


if __name__ == "__main__":
    main()
