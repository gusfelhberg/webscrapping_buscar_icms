from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import sys

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lista_ufs=["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]
lista_meses=["01","02","03","04","05","06","07","08","09","10","11","12"]
listas = []

def busca_icms(uf):

    url_base = 'https://www.confaz.fazenda.gov.br/legislacao/boletim-do-icms/'

    for ano in range(2013,2018):
        for mes in lista_meses:
            print(uf+' - '+mes+'/'+str(ano))

            html_doc = requests.get(url_base + nome_tributo + '/' + uf + '/' + str(ano) + mes,verify=False)
            soup = html_doc.content
            soup = BeautifulSoup(soup, 'html.parser')

            core = soup.find("div",{"id":"content-core"})
            core = soup.find_all("div",{"id":"content-core"})
            cor = core[0].find_all("div",{"class":"field"})

            lst=[]
            for c in cor:
                a = c.text.replace("\n",";").replace("\t","").replace("\xa0","").replace("        ","").replace("  ","").replace(";;",";")[:-1]
                if a[1] == '1' or a[1] =='2':
                    b = a[1:]
                    lst.append(b.split(";")[0])
                    lst.append(b.split(";")[1].replace("R$ ",""))
                    lst.append(ano)
                    lst.append(mes)
                    lst.append(uf)
                    lst.append("ICMS")
                    lst.append(url_base + nome_tributo + '/' + uf + '/' + str(ano) + mes)
                    listas.append(lst)
                    lst=[]


for uf in lista_ufs:
    busca_icms(uf)
    # print(listas)

labels = ["Item","Valor","Ano","Mes","UF","Tributo","URL"]

icms = pd.DataFrame(listas,columns=labels)
icms = icms.set_index("Item")

writer = pd.ExcelWriter('icms.xlsx', engine='xlsxwriter')
icms.to_excel(writer, sheet_name='ICMS')
writer.save()

print(icms)
