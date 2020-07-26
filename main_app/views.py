import requests
import json
from django.shortcuts import render

def get_tmc(monto, plazo):

     #logica a implementar
     #tipo_tmc = '35' for testing
     if int(plazo) <= 90:
        if int(monto) <= 5000:
           tipo_tmc = '26';
        elif int(monto) > 5000:
           tipo_tmc = '25'
     elif int(plazo) > 90:
        if int(monto) <= 50:
           tipo_tmc = '45'
        elif int(monto) > 5000:
           tipo_tmc = '34'
        elif int(monto) > 50:
            if int(monto) < 200:
               tipo_tmc = '44'
            if int(monto) < 5000:
               tipo_tmc = '35'
  
     return (tipo_tmc)

def remove_char(s):
    return s[1 : -1]

def home(request):
#    response = requests.get('https://jsonplaceholder.typicode.com/todos/')
#    todos = response.json()
#    return render(request, "main_app/home.html", {"data": todos})
    
    #response = requests.get('https://api.sbif.cl/api-sbifv3/recursos_api/tmc/2020?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=JSON')
    #response = requests.get('https://api.sbif.cl/api-sbifv3/recursos_api/tmc/posteriores/2020/06?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json')
	#calling_url = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/2020/07?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json'

    tmcs = {}
    valor_tmc_resultado = 0
    tipo_tmc_esperada = ''
    valor_fecha_desde = ''
    valor_fecha_hasta = ''

    if 'fechax' in request.GET:

        fechax = request.GET['fechax']
        #DD-MM-AAAA
        param_anio = fechax[-4:]
        print(param_anio)
        param_mes = fechax[3:5]
        print(param_mes)
        param_dia = fechax[0:2]
        print(param_dia)
        if int(param_dia) <= 15: #request con param_mes=mes-1
            #ojo, controlar cuando el mes es: 10, 11, 12 y cuando mes es 01
            print('0'+str(int(param_mes)-1))
            calling_url = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/{}/{}?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json'.format(param_anio,'0'+str(int(param_mes)-1))
            response = requests.get(calling_url)
        elif int(param_dia) > 15: #request con param_mes=mes
            calling_url = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/{}/{}?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json'.format(param_anio,param_mes)
            response = requests.get(calling_url)
        tmcs = response.json()

        monto_verificar = request.GET['monto']
        plazo_verificar = request.GET['plazo']
        tipo_tmc_esperada = get_tmc(monto_verificar, plazo_verificar)

        print("monto:", monto_verificar)
        print("plazo:", plazo_verificar)
        print("tipo_tmc:" , tipo_tmc_esperada)




        tmcs_list = tmcs["TMCs"] #sacando root element


        #recorriendo la tupla
        for tmc in tmcs_list:
            print("tmc:{} ".format(tmc))
            dic_tmc = dict(tmc)
            items = dic_tmc.items()
            for key in tmc:
                print(key, ":", tmc[key])
            dic_tmc = dict(tmc)
            keys = dic_tmc.keys()
            print(keys)
            valor_tipo = dic_tmc.get('Tipo')
            if valor_tipo == tipo_tmc_esperada:
                 #print('PROCESO FUNCIONA')
                 #encontrado tipo_tmc
                 valor_tmc_resultado = dic_tmc.get('Valor')
                 valor_fecha_desde = dic_tmc.get('Fecha')
                 valor_fecha_hasta = dic_tmc.get('Hasta')

    return render(request, "main_app/home.html", {
                   "data": tmcs,
                   'tmc_buscada': valor_tmc_resultado,
                   'tipo_tmc_encontrada': tipo_tmc_esperada,
                   'fecha_desde': valor_fecha_desde,
                   'fecha_hasta': valor_fecha_hasta
                  })


