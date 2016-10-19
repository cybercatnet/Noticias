import urllib.request
import re
import os
import json
import xml.etree.ElementTree as ET
import xml.sax


def formatear(texto=""):
    def claveAValor(m):

        print(m)

        if m[0] == "<" and m[len(m) - 1] == ">":
            return ""

        if m in dicc:

            return dicc[m]

        # return "FALTA VALOR " + m

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

    dicc[r'\n'] = ""
    dicc[r'\r'] = ""
    dicc[r'\t'] = ""
    dicc[r'  '] = ""

    dicc[r'!'] = ""
    dicc[r'('] = ""
    dicc[r')'] = ""
    dicc[r'\''] = ""
    dicc[r'.'] = ""
    dicc[r','] = ""
    dicc[r':'] = ""
    dicc[r';'] = ""
    dicc[r'|'] = ""
    dicc[r'"'] = ""
    dicc[r'='] = ""
    dicc[r'&'] = ""

    return re.sub(r'\\x\w\w\\x\w\w|\\U\w{8}|\\u\w{4}|\\x\w\w|\\n|\\t|\\r|\'|\.|\"|\,|\:|\;|\||\@\w+(?=\W)|\#\w+(?=\W)|https?\S+(?=\W)|[A-Z]|\s\s|\!|\(|\)|\<\/?(\w|\s)*\>|\=|\&', lambda m: claveAValor(m.group(0)), texto)


def cargarRSS(RSS):
    dict = {}
    if os.path.exists(RSS):
        with open(RSS, "r") as RSS:
            dict = json.load(RSS)
    return dict


def main():
    RSS = cargarRSS("RSS.py")
    for diario in RSS:
        for seccion in RSS[diario]:
            print(RSS[diario][seccion])
            with urllib.request.urlopen(urllib.request.Request(RSS[diario][seccion])) as url:
                root = ET.parse(url).getroot()
                print(xml.sax.parseString(url))
                print(root.findall(".//entry"))


if __name__ == "__main__":
    main()
