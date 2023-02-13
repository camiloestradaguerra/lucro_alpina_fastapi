import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime
import pandas as pd

def _todas_las_ciudades():
    path = os.getcwd()
    driver_path = '{}\chromedriver'.format(path)    
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get("https://alpina.com/")
    
    driver.maximize_window() 
    time.sleep(1)
    foto_list = []
    link_articulos = []
    siguiente_list = []
    nombre_list = []
   
    ciudades_list = []
    fechas_list = []
    ean = []
    precio_actual = []
    precio_real = []
    promocion = []
    unidad_de_medida = []
    cantidad = []
    categoria = []
    marca = []
    descripcion = []
    time.sleep(1)
    try:
        time.sleep(1)
        boton_ciudades = driver.find_element(By.XPATH, '//*[@id="store-switcher"]/a').click()
    except:
        try:
            time.sleep(1)
            boton_ciudades = driver.find_element(By.XPATH, '//*[@id="store-switcher"]/a').click()
        except:
            pass
            
    time.sleep(1)
    try:
        time.sleep(1)
        lista_ciudades =  driver.find_elements(By.XPATH,'//*[@id="store-switcher"]/div[1]/div/ul/li/input')
    except:
        try:
            lista_ciudades =  driver.find_elements(By.XPATH,'//*[@id="store-switcher"]/div[1]/div/ul/li/input')
        except:
            pass

    for i in range(0, len(lista_ciudades)):
        
        try:
            time.sleep(1)
            ciudad_link = driver.find_elements(By.XPATH,'//*[@id="store-switcher"]/div[1]/div/ul/li/input')[i].get_attribute("data-url")
            time.sleep(1)
            driver.get(ciudad_link)
        except:
            pass
        
        time.sleep(1)
        
        a = 1
        b = 0
        
        while a > b:
            time.sleep(1)

            nombres = driver.find_elements(By.XPATH, '//div[@class="product-item-name"]')
            for nombre in nombres:
                nombre_list.append(nombre.text)
             
            time.sleep(1)
            
            fotos = driver.find_elements(By.XPATH, '//img[@class="product-image-photo"]')
            for foto in fotos:
                foto_list.append(foto.get_attribute('src'))
            
            time.sleep(1)
            
            articulos = driver.find_elements(By.XPATH, '//a[@class="product-item-link"]')
            
            time.sleep(1)
            
            for articulo in articulos:
                time.sleep(1)
                link_articulos.append(articulo.get_attribute('href'))
            
            ciudad_text = [driver.find_element(By.XPATH, '//div[@class="store-switcher-container"]/a').text for i in range(0, len(nombres))]
            ciudades_list = ciudades_list + ciudad_text
            
            fecha_ejecucion = [datetime.today().strftime('%m-%d') for i in range(0, len(nombres))]
            fechas_list = fechas_list + fecha_ejecucion
             
           # Boton Siguiente
            try:
                driver.get(driver.find_element(By.XPATH, '//a[@class="action  next"]').get_attribute("href"))
            except:
                a = -1
                  
    for link in link_articulos:
            
        time.sleep(3)
            
        try:
            driver.get(link)
        except:
            pass
            
        try:
            ean.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[3]/div[2]/div').text)    
        except:
            ean.append(' ')
            
        time.sleep(1)
            
        try:
            descripcion.append(driver.find_element(By.XPATH, '//*[@id="description"]/div/div[@class="value"]').text)
        except:
            descripcion.append(driver.find_element(By.XPATH, '//div[@class="product attribute overview"]/div').text)
          
        time.sleep(1)
            
        try:
            cantidad.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[4]/div[3]/div[2]/div').text)
        except:
            cantidad.append(' ')
                
        time.sleep(1)
            
        try:
            unidad_de_medida.append(driver.find_element(By.XPATH, '//div[@class="product attribute measurement unit type"]/div').text)
        except:
            unidad_de_medida.append(' ')
            
        time.sleep(1)
            
        try:
            promocion.append(driver.find_element(By.XPATH,'//div[@class="discount"]/span').text[:-1])
        except:
            promocion.append('0')
            
        time.sleep(1)
            
        try:
            precio_actual.append(driver.find_element(By.XPATH,'//span[@data-price-type="finalPrice"]/span[@class="price"]').text.replace('.', ''))
        except:
            precio_actual.append(' ')
            
        time.sleep(1)
            
        try:
            precio_real.append(driver.find_element(By.XPATH,'//span[@data-price-type="oldPrice"]/span[@class="price"]').text.replace('.', ''))
        except:
            try:
                time.sleep(1)
                precio_real.append(driver.find_element(By.XPATH,'//span[@data-price-type="finalPrice"]/span[@class="price"]').text.replace('.', ''))
            except:
                precio_real.append(' ')
            
        time.sleep(1)
            
        try:
            categoria.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[7]/div/div/div[2]').text.replace('\n', ', '))    
        except:
            categoria.append(' ')
            
        time.sleep(1)
            
        try:
            marca.append(driver.find_element(By.XPATH, '//*[@id="store.menu"]/div/div[1]/div[1]/div[2]/ul/li[2]/div/ul/li[1]/a').text)    
        except:
            marca.append(' ')
            
        time.sleep(1)

    compania = ['Alpina' for i in range(0, len(link_articulos))]

    datos_productos = {'Fecha' : fechas_list, 'Ciudad' : ciudades_list, 'Nombre' : nombre_list, 'Precio Real' : precio_real, 'Precio Actual' : precio_actual, 'Promocion' : promocion, 
                       'url' : link_articulos, 'ean': ean, 'Unidad de Medida' : unidad_de_medida, 'Cantidad' : cantidad, 'Marca' : marca, 'Compañia' : compania,
                       'Categoria': categoria, 'Descripcion' : descripcion}
    
    datos_productos_df = pd.DataFrame(datos_productos) 
    datos_productos_df.to_csv('todas_las_ciudades.csv', encoding='utf-8-sig', index=False)
  
    return datos_productos

