import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime
import pandas as pd


def _ciudad_individual(numero_de_ciudad : str):
    path = os.getcwd()
    driver_path = '{}\chromedriver'.format(path)    
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s)
    driver.get("https://alpina.com/")
    driver.maximize_window() 

    boton_ciudades = driver.find_element(By.XPATH, '//*[@id="store-switcher"]/a').click()
    
    time.sleep(1)    
    
    lista_ciudades = driver.find_elements(By.XPATH, '//input[@name="store"]')
    
    time.sleep(1)
    
    ciudad = lista_ciudades[numero_de_ciudad].click() 
    
    time.sleep(1)
    
    driver.find_element(By.XPATH, '//*[@id="store-switcher"]/div[1]/div/button').click()
    
    time.sleep(1)
    
    try:
        link_todos = driver.find_element(By.XPATH, '//a[@class="level-top  category-node-100"]').get_attribute('href')
        driver.get(link_todos)
    except:
        try:
            time.sleep(1)

            link_todos = driver.find_element(By.XPATH, '//a[@class="level-top  category-node-100"]').get_attribute('href')
            driver.get(link_todos)
        except:
            pass
        
    time.sleep(1)

    try:
        boton_productos = driver.find_element(By.XPATH, '//*[@id="header-custom"]/div/div[1]/span').click()
    except:
        try: 
            boton_productos = driver.find_element(By.XPATH, '//*[@id="header-custom"]/div/div[1]/span').click() 
        except:
            pass
          
    time.sleep(1)

    try:
        todos = driver.find_element(By.XPATH, '//*[@id="store.menu"]/div/div[1]/div[1]/div[2]/ul/li[1]/a').click()
    except:
        try:
            todos = driver.find_element(By.XPATH, '//*[@id="store.menu"]/div/div[1]/div[1]/div[2]/ul/li[1]/a').click()
        except:
            pass
            
    time.sleep(1)
      
    #Caracteristicas de los productos
    
    foto_list = []
    link_articulos = []
    siguiente_list = []
    nombre_list = []
    
    ean = []
    precio_actual = []
    precio_real = []
    promocion = []
    unidad_de_medida = []
    cantidad = []
    categoria = []
    marca = []
    descripcion = []
    
    a = 1
    b = 0
    
    while a > b:
       
        time.sleep(0.5)

        nombres = driver.find_elements(By.XPATH, '//div[@class="product-item-name"]')
        for nombre in nombres:
            nombre_list.append(nombre.text)
            
        time.sleep(0.5)
        
        fotos = driver.find_elements(By.XPATH, '//img[@class="product-image-photo"]')
        for foto in fotos:
            foto_list.append(foto.get_attribute('src'))
            
        time.sleep(0.5)

        articulos = driver.find_elements(By.XPATH, '//a[@class="product-item-link"]')
        for articulo in articulos:
            link_articulos.append(articulo.get_attribute('href'))
            
        time.sleep(0.5)

        try:
            driver.get(driver.find_element(By.XPATH, '//a[@class="action  next"]').get_attribute("href"))
        except:
            a = -1
    
    for link in link_articulos:
        
        time.sleep(0.5)

        try:
            driver.get(link)
        except:
            pass
        
        try:
            ean.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[3]/div[2]/div').text)    
        except:
            ean.append(' ')
        
        time.sleep(0.5)

        try:
            descripcion.append(driver.find_element(By.XPATH, '//*[@id="description"]/div/div[@class="value"]').text)
        except:
            descripcion.append(driver.find_element(By.XPATH, '//div[@class="product attribute overview"]/div').text)
      
        time.sleep(0.5)

        try:
            cantidad.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[4]/div[3]/div[2]/div').text)
        except:
            cantidad.append(' ')
            
        time.sleep(0.5)

        try:
            unidad_de_medida.append(driver.find_element(By.XPATH, '//div[@class="product attribute measurement unit type"]/div').text)
        except:
            unidad_de_medida.append(' ')
        
        time.sleep(0.5)

        try:
            promocion.append(driver.find_element(By.XPATH,'//div[@class="discount"]/span').text)
        except:
            promocion.append('0')
        
        time.sleep(0.5)

        try:
            precio_actual.append(driver.find_element(By.XPATH,'//span[@data-price-type="finalPrice"]/span[@class="price"]').text[2:-3].replace('.', ''))
        except:
            precio_actual.append(' ')
        
        time.sleep(0.5)
        
        try:
            precio_real.append(driver.find_element(By.XPATH,'//span[@data-price-type="oldPrice"]/span[@class="price"]').text[2:-3].replace('.', ''))
        except:
            try:
                precio_real.append(driver.find_element(By.XPATH,'//span[@data-price-type="finalPrice"]/span[@class="price"]').text[2:-3].replace('.', ''))
            except:
                precio_real.append(' ')
        
        time.sleep(0.5)
        
        try:
            categoria.append(driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[7]/div/div/div[2]').text.replace('\n', ', '))    
        except:
            categoria.append(' ')
        
        time.sleep(0.5)
        
        try:
            marca.append(driver.find_element(By.XPATH, '//*[@id="store.menu"]/div/div[1]/div[1]/div[2]/ul/li[2]/div/ul/li[1]/a').text)    
        except:
            marca.append(' ')
        
        time.sleep(0.5)
    
    ciudad = [driver.find_element(By.XPATH, '//a[@class="switcher-current js-open-modal"]').text for i in range(0, len(link_articulos))]
    fecha = [datetime.today().strftime('%m-%d') for i in range(0, len(link_articulos))]
    compania = ['Alpina' for i in range(0, len(link_articulos))]
    datos_productos = {'Fecha' : fecha, 'Ciudad' : ciudad, 'Nombre' : nombre_list, 'Precio Real' : precio_real, 'Precio Actual' : precio_actual, 'Promocion' : promocion, 
                       'url' : link_articulos, 'ean': ean, 'Unidad de Medida' : unidad_de_medida, 'Cantidad' : cantidad, 'Marca' : marca, 'Compañia' : compania,
                       'Categoria': categoria, 'Descripcion' : descripcion}
    
    datos_productos_df = pd.DataFrame(datos_productos) 
    n_ciudad = 'df_'+str(ciudad[0])+'.csv'
    datos_productos_df.to_csv(n_ciudad, encoding='utf-8-sig', index=False)

    return datos_productos

