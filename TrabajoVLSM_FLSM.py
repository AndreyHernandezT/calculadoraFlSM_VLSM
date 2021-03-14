def decimal_binario(lista_decimal):   #Funcion para generar el número binario a través del numero decimal
    try:
        decimal = int(lista_decimal) 
        binario = f'{int(decimal):b}'
        return binario
    except:
        lista_binario = []
        for i in range(len(lista_decimal)):
            binario = f'{int(lista_decimal[i]):b}'
            lista_binario.append(binario)
        return lista_binario
    
def unir_listas(lista):
    for i in range(len(lista)):
        lista[i] = str(lista[i])
    separador = "."
    return (separador.join(lista))

def binario_decimal(lista_binario):
    try:
        decimal = int(lista_binario,2) 
        return decimal
    except:
        lista_decimal = []
        for i in range(len(lista_binario)):
            decimal = int(lista_binario[i],2) 
            lista_decimal.append(decimal)
        return lista_decimal

def arreglar_direccion(dir_binaria):
    for i in range(4):
        if len(dir_binaria[i]) == 1:
            dir_binaria[i] = '0'*8
    return dir_binaria

def direccion_mascara(prefijo): #Funcion para retornar la direccion de la mascara de red
    lista_mascara = [0]*32
    lista_listas_mascara = [0]*4
    for i in range(prefijo):
        lista_mascara[i] = 1
    for i in range(4):
        salto_1 = i*8
        salto_2 = ((i*2)+2)*4
        x = "".join(([str(i) for i in lista_mascara[salto_1:salto_2]])) 
        lista_listas_mascara[i] = x
    lista_mascara = [0]*4
    for i in range(len(lista_mascara)):
        lista_mascara[i] = "".join(lista_listas_mascara[i])
    return lista_mascara

def operacion_and(lista_direccionesIP, lista_mascara): # Funcion que genera el resultado de la direccion IP
    lista_direccionRed = []                            # con la direccion de la mascara de red 
    for i in range(len(lista_mascara)):
        lista_direccionRed.append(int(lista_direccionesIP[i], 2) & int(lista_mascara[i], 2))
    return decimal_binario(lista_direccionRed)

def clase_direccion(dir_binaria):
    clase_ip = ''
    if int(dir_binaria[0], 2) < 128 : clase_ip = 'A'
    elif int(dir_binaria[0], 2) < 192 : clase_ip = 'B'
    elif int(dir_binaria[0], 2) < 224 : clase_ip = 'C'
    return clase_ip
    
def funcion_FLSM(dir_binaria, prefijo, redes):
    adicional = len(decimal_binario(redes))
    prefijo += adicional
    nueva_direccion_masc = direccion_mascara(prefijo)
    dir_binaria_operada = operacion_and(dir_binaria, nueva_direccion_masc)
    #print(nueva_direccion_masc)
    lista_primera_dir = arreglar_direccion(dir_binaria_operada) 
    for i in range(3,0,-1):
        if int(nueva_direccion_masc[i], 2) < 255:
            bandera = True
            j = 7
            while bandera:
                if nueva_direccion_masc[i][j] == '1':
                    lista_primera_dir[i] = f'{int(2**(7-j)):b}'
                    bandera = False
                j -= 1
                if j < 0:
                    break
    return lista_primera_dir, nueva_direccion_masc, prefijo

def calculo_FLSM(direccion, redes):
    prefijo_mascara = direccion.split('/')
    direccion_IP = prefijo_mascara[0].split('.')
    dir_binaria = decimal_binario(direccion_IP)
    lista_mascara = direccion_mascara(int(prefijo_mascara[1])) 
    prefijo = int(prefijo_mascara[1])

    lista_primera_dir, nueva_direccion_masc, prefijo_nuevo = funcion_FLSM(dir_binaria, prefijo, redes)
 
    if clase_direccion(lista_primera_dir) == 'B':
        lista_inicial_decimal = binario_decimal(lista_primera_dir)
        direccion_inicial = str(lista_inicial_decimal[0])+'.'+str(lista_inicial_decimal[1])+'.'
        salto_red = 256 - int(nueva_direccion_masc[2],2)
        host = 2
        incremento_red = 0
        incremento_host = host
        print("\nDirección Clase B")
        for red in range(redes):
            print("\nRed Número ",(red+1))
            print("\tDirección de red: ", direccion_inicial+str(incremento_red)+'.'+str(lista_inicial_decimal[3])+'.'+prefijo_nuevo)
            print("\tMascara de red: ", binario_decimal(nueva_direccion_masc))
            print("\tPrimera Direccion Utilizable: ", direccion_inicial+str(incremento_red)+'.'+str(lista_inicial_decimal[3]+1))
            print("\tUltima Direccion Utilizable: ", direccion_inicial+str((incremento_red+salto_red)-1)+'.'+str(254))
            print("\tDireccion Broadcast: ", direccion_inicial+str((incremento_red+salto_red)-1)+'.'+str(255))
            incremento_red += salto_red

    if clase_direccion(lista_primera_dir) == 'C':
        lista_inicial_decimal = binario_decimal(lista_primera_dir)
        direccion_inicial = str(lista_inicial_decimal[0])+'.'+str(lista_inicial_decimal[1])+'.'+ str(lista_inicial_decimal[2])+'.'
        salto_red = 256 - int(nueva_direccion_masc[3],2)
        incremento_host = salto_red - 2
        incremento_red = 0
        print("\nDirección Clase C")
        for red in range(redes):
            print("\nRed Número ",(red+1))
            print("\tDirección de red: ", direccion_inicial+str(incremento_red))
            print("\tMascara de red: ", binario_decimal(nueva_direccion_masc))
            print("\tPrimera Direccion Utilizable: ", direccion_inicial+str(incremento_red+1))
            print("\tUltima Direccion Utilizable: ", direccion_inicial+str(incremento_host))
            print("\tDireccion Broadcast: ", direccion_inicial+str(incremento_host+1))
            incremento_red += salto_red
            incremento_host += salto_red

def funcion_VLSM(direccion, hosts):
    mascara = '1'*16
    i = 0
    prestados = 0
    primera = direccion[:4]
    primera[3] += 1
    while True:
        posibles = 2**i
        if (posibles - 2) >= hosts:
            ceros = '0'*i
            prestados = 16-i
            unos = '1'*prestados
            mascara += unos+ceros
            break     
        i += 1
    prefijo = '1'*16
    prefijo += '1'*prestados
    mascara_nueva = [mascara[0:8], mascara[8:16], mascara[16:24], mascara[24:32]]
    mascara_deci = binario_decimal(mascara_nueva)
    
    ultima = []
    broadcast = []
    j = 3
    while True:
        
        if mascara_deci[j] < 255 and mascara_deci[j] > 0:
            
            """ ultima = direccion[:4]
            broadcast = direccion[:4]
            ultima[2] -= 1
            ultima[3] = 254
            broadcast[2] = ultima[2]
            broadcast[3] = 255
            break """
            salto_red = 256 - mascara_deci[j]
            direccion[j] += salto_red
            ultima = direccion[:4]
            broadcast = direccion[:4]
            if j == 2:
                ultima[j] -= 1
                ultima[3] = 254
                broadcast[j] -= 1
                broadcast[3] = 255
            else:
                ultima[j] -=2
                broadcast[j] -=1
            break
        j -= 1
    if direccion[3] > 254:
        direccion[3] = 0
        direccion[2]+=1
    print("\tMascara de red: ", unir_listas(mascara_deci) +'\tPrefijo:  /'+str(len(prefijo)))
    print("\tPrimera Direccion Utilizable : ",unir_listas(primera))
    print("\tUltima Direccion Utilizable: ",unir_listas(ultima))
    print("\tDireccion de Broadcast: ",unir_listas(broadcast))

    return direccion

salir = False
opcion = 0
while not salir:
    print("1. Realizar el calculo por FLSM")
    print("2. Realizar el calculo por VLSM")
    print("3. Salir")
    opcion = int(input("Elija la opción: "))

    if opcion == 1:
        print("Selecciono el caclulo por FLSM\n")
        direccion = input("Ingrese la direccion de red: ")
        redes = int(input("Ingrese la cantidad de redes: "))
        hosts = int(input("Ingrese la cantidad de hosts: "))

        calculo_FLSM(direccion, redes)

    elif opcion == 2:
        print("Selecciono el caclulo por VLSM\n")
        direccion_inicial = input("Ingrese la direccion de red: ")
        redes = int(input("Ingrese la cantidad de redes: "))
        lista_hosts= []
        for i in range(redes):
            hosts = int(input("Ingrese los host DE MAYOR A MENOR para la red Numero "+ str(i+1) +": "))
            lista_hosts.append(hosts)

        prefijo_mascara = direccion_inicial.split('/')
        direccion = prefijo_mascara[0].split('.')
        prefijo = int(prefijo_mascara[1])

        for i in range(len(direccion)):
                direccion[i] = int(direccion[i])

        for red in range(redes):
            print("\nRed Número ",(red+1))
            print("\tDirección de red: ", unir_listas(direccion[:4]))
            direccion = funcion_VLSM(direccion, lista_hosts[red])
    elif opcion == 3:
        print("Adios!") 
        salir = True
    else:
        print("Opcion inválida, vuelva a intentarlo")