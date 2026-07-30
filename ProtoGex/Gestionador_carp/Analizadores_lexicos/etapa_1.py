def linea(texto):
        
    linea = []
    codigo = []
    
    numero_de_linea = 1
    
    for c in texto:
        if c == "\n":
            if linea:
                letras = False
                for c2 in linea:
                    if c2 not in (" ", "\t"):
                        letras = True
                        break
                    else:
                        continue
                if not letras:
                    codigo.append(["NULO", numero_de_linea])
                else:
                    codigo.append([linea, numero_de_linea])
                linea = []
            else:
                codigo.append(["NULO", numero_de_linea])
            numero_de_linea+=1
            continue
        linea.append(c)
    if linea:
        letras = False
        for c2 in linea:
            if c2 not in (" ", "\t"):
                letras = True
                break
            else:
                continue
        if not letras:
            codigo.append(["NULO", numero_de_linea])
        else:
            codigo.append([linea, numero_de_linea])
    linea = None
    numero_de_linea = None
    
    return ["OK", codigo]
