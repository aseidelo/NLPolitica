import requests
import re
import html2text
from bs4 import BeautifulSoup as bs
import pandas as pd

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.ignore_tables = True
text_maker.ignore_images = True
text_maker.ignore_anchors = True
text_maker.ignore_emphasis = True
text_maker.body_width = 0

atas = ["DAR-I-001 - 16 DE SETEMBRO DE 2020.txt",
		"DAR-I-009 - 2 DE OUTUBRO DE 2020.txt",
		"DAR-I-002 - 17 DE SETEMBRO DE 2020.txt",
		"DAR-I-010 - 7 DE OUTUBRO DE 2020.txt",
		"DAR-I-003 - 18 DE SETEMBRO DE 2020.txt",
		"DAR-I-011 - 8 DE OUTUBRO DE 2020.txt",
		"DAR-I-004 - 23 DE SETEMBRO DE 2020.txt",
		"DAR-I-012 - 9 DE OUTUBRO DE 2020.txt",
		"DAR-I-005 -24 DE SETEMBRO DE 2020.txt",
		"DAR-I-006 - 25 DE SETEMBRO DE 2020.txt",
		"DAR-I-013 - 14 DE OUTUBRO DE 2020.txt",
		"DAR-I-007 - 30 DE SETEMBRO DE 2020.txt",
		"DAR-I-008 - 1 DE OUTUBRO DE 2020.txt"]

path_to_dataset = "atas_assembleia-pt/txt/"
initiatives = "https://www.parlamento.pt/ActividadeParlamentar/Paginas/DetalheIniciativa.aspx?"

urls = []
for ata in atas:
	with open("{}{}".format(path_to_dataset, ata), 'r') as file:
		for line in file:
			for m in re.finditer(initiatives, line):
				url = line[m.start(): m.end() + 9]
				#print(url)
				if(url not in urls):
					urls.append(url)
print(len(urls))
#url = "https://www.parlamento.pt/ActividadeParlamentar/Paginas/IniciativasLegislativas.aspx"
titles = []
descriptions = []
authors = []
to_save_urls = []
for url in urls:
	try:
		res = requests.get(url)
		html = res.text
		soup = bs(html, 'html.parser')
		title=soup.find('span', attrs={'id':'ctl00_ctl52_g_951a642c_ced8_43d8_af6a_57edb1db8006_ctl00_lblTitulo'}).text.replace('\n', '').replace('\r', '').replace('  ', '')
		description = soup.find('span', attrs={'id':'ctl00_ctl52_g_951a642c_ced8_43d8_af6a_57edb1db8006_ctl00_ucLinkDocumento_lblDocumento'}).text.replace('\n', '').replace('\r', '').replace('  ', '')
		author = soup.find('div', attrs={'id':'ctl00_ctl52_g_951a642c_ced8_43d8_af6a_57edb1db8006_ctl00_pnlAutoresD'}).text.replace('\n', '').replace('\r', '').replace('  ', '')
		titles.append(title)
		descriptions.append(description)
		authors.append(author)
		to_save_urls.append(url)
		print("{} | {} | {} | {}".format(title, description, author, url))
	except:
		pass
df = pd.DataFrame({'title': titles, 'description' : descriptions, 'author': authors, 'url' : to_save_urls})
df.to_csv('projetos_assembleia.csv', index=False)
#https://www.parlamento.pt/ActividadeParlamentar/Paginas/DetalheIniciativa.aspx?BID=45187

