from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from pathlib import Path
import time, csv, os

resultado = {}
FilePath = str(Path.home()) + '/resultados.csv'

try:
	options = Options()
	options.add_argument("--headless")
	browser = webdriver.Firefox(options=options)

	browser.get(r'https://www.brasilbandalarga.com.br/bbl/')
	time.sleep(5)

	horaInicioTeste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	browser.find_element_by_id('btnIniciar').click()
	time.sleep(3)

	while True:
		if "Teste Finalizado" in browser.page_source:
			horaFimTeste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			break
		else:
			time.sleep(5)

	DownAndUp = browser.find_elements_by_class_name("textao")
	Manyresults = browser.find_elements_by_xpath("//*[@class='col-xs-6 col-md-6']")
	ServerTeste = browser.find_element_by_xpath("//*[@class='col-xs-6 col-md-6 text-center']")

	resultado["Download"] = DownAndUp[0].text
	resultado["Upload"] = DownAndUp[1].text
	resultado['Hora de inicio'] = horaInicioTeste
	resultado['Hora de termino'] = horaFimTeste
	resultado['Latencia'] = Manyresults[3].text
	resultado['Jitter'] = Manyresults[5].text
	resultado['Perda'] = Manyresults[7].text
	resultado['IP'] = Manyresults[9].text
	resultado['Servidor de Teste'] = ServerTeste.text
	resultado['Região servidor'] = Manyresults[11].text
	resultado['Região Teste'] = Manyresults[11].text

	if not os.path.isfile(FilePath):
		with open(FilePath, 'w', newline="") as ResultsFile:
			writer=csv.DictWriter(ResultsFile, fieldnames=["Download", "Upload", "Hora de inicio", "Hora de termino", "Latência", "Jitter", "Perda", "IP", "Servidor de Teste", "Região servidor", "Região Teste"])
			writer.writeheader()
			writer.writerow(resultado)
	else:
		with open(FilePath, 'a+', newline='') as ResultsFile:
			writer = csv.writer(ResultsFile)
			writer.writerow(resultado.values())

except Exception as error:
	print(error)
	browser.close()

finally:
	browser.close()
