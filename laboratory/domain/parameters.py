# Parámetros físico-químicos
FQ_PARAMETERS = [
    "Temperatura",
    "pH",
    "Cloro residual libre",
    "Alcalinidad total",
    "Aluminio residual",
    "Calcio",
    "Cloruros",
    "Color aparente",
    "Conductividad",
    "Dureza total",
    "Fosfato",
    "Hierro total",
    "Magnesio",
    "Nitrito",
    "Sólidos disueltos totales",
    "Sulfatos",
    "Turbiedad",
    "Amonio",
    "DQO",
    "Dureza cálcica",
    "Fenol",
    "Fluoruro",
    "Manganeso",
    "Nitrato",
    "Oxígeno disuelto",
]

# Parámetros microbiológicos
MICRO_PARAMETERS = [
    "Coliformes totales",
    "Escherichia coli",
    "Mesófilos aerobios",
]

#Unidades
UNIDADES = {
        "Temperatura":"°C",
        "pH":"Unidades",
        "Cloro residual libre":"mg Cl₂/L",
        "Alcalinidad total":"mg CaCO₃/L",
        "Aluminio residual":"mg Al/L",
        "Calcio":"mg Ca/L",
        "Cloruros":"mg Cl/L",
        "Color aparente":"UPC",
        "Conductividad":"µS/cm",
        "Dureza total":"mg CaCO₃/L",
        "Fosfato":"mg PO₄³/L",
        "Hierro total":"mg Fe/L",
        "Magnesio":"mg Mg/L",
        "Nitrito":"mg NO₂/L",
        "Sólidos disueltos totales":"mg/L",
        "Sulfatos":"mg SO₄²/L",
        "Turbiedad":"UNT",
        "Amonio":"mg NH₄⁺/L",
        "DQO":"mg O₂/L",
        "Dureza cálcica":"mg CaCO₃/L",
        "Fenol":"mg C₆H₅OH/L",
        "Fluoruro":"mg F⁻/L",
        "Manganeso":"mg Mn/L",
        "Nitrato":"mg NO₃⁻/L",
        "Oxígeno disuelto":"mg OD/L",
        "Coliformes totales": "NMP/100mL", 
        "Escherichia coli": "NMP/100mL", 
        "Mesófilos aerobios": "UFC/mL"
}

#Tipos de muestras
TIPOS_MUESTRA = [
    "",
    "Interna",
    "Externa",
    "Red"
]

#Puntos de red
PUNTOS_RED = [
    "San Cristóbal", 
    "Silveria Espinoza", 
    "Santa Rita", 
    "Copihue", 
    "Alcaldía",
    "Girardot",
    "Arboleda", 
    "Manablanca", 
    "Carcel de la policia", 
    "Batallón",
    "Universidad", 
    "Coliseo", 
    "Brasilia", 
    "Hospital", 
    "SENA", 
    "Prado",
    "Pueblo Viejo", 
    "Villa Olímpica"
]

#Dispositivos de toma
DISPOSITIVOS_TOMA = [
    "", 
    "Manguera", 
    "Canal", 
    "Grifo", 
    "Otro"
]

#Tipos de agua
TIPOS_AGUA = [
    "", 
    "Agua potable (AP)", 
    "Agua superficial (ASP)",
    "Agua subterránea (ASB)", 
    "Agua envasada (AE)",
    "Agua lluvia (AL)", 
    "Otra (O)"
]

#Fuentes de abastecimiento
FUENTES_ABASTECIMIENTO = [
    "", 
    "Andes Medio", 
    "Mancilla Bajo", 
    " Botello Alto", 
    "San Rafael I", 
    "San Rafael II", 
    "Deudoro Aponte", 
    "Manablanca",
    "Cartagenita",
    "Guapucha II",
    "Gatillo 0",
    "Gatillo 1", 
    "Gatillo 2",
    "Gatillo 3"
]

MESES = {
    "01": "Enero",
    "02": "Febrero",
    "03": "Marzo",
    "04": "Abril",
    "05": "Mayo",
    "06": "Junio",
    "07": "Julio",
    "08": "Agosto",
    "09": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre",
}

NORMA_CUMPLIMIENTO = {
    "pH" : {
        "type" : "range",
        "min" : 6.5,
        "max" : 9.0
    },
    "Cloro residual libre":{
        "type" : "range",
        "min" : 0.3,
        "max" : 2.0
    },
    "Alcalinidad total":{
        "type" : "exact",
        "value": 200
    },
    "Aluminio residual":{
        "type" : "exact",
        "value": 0.2
    },
    "Calcio":{
        "type" : "exact",
        "value" : 60
    },
    "Cloruros":{
        "type" : "exact",
        "value": 250
    },
    "Color aparente":{
        "type" : "exact",
        "value" : 15
    },
    "Conductividad":{
        "type" : "exact",
        "value" : 1000
    },
    "Dureza total":{
        "type" : "exact",
        "value" : 300
    },
    "Fosfato":{
        "type" : "exact",
        "value" : 0.5
    },
    "Hierro total":{
        "type" : "exact",
        "value" : 0.3
    },
    "Magnesio":{
        "type" : "exact",
        "value" : 36
    },
    "Nitrito":{
        "type" : "exact",
        "value" : 0.1
    },
    "Sulfatos":{
        "type" : "exact",
        "value" : 250
    },
    "Turbiedad":{
        "type" : "exact",
        "value" : 2
    },
    "Fluoruro":{
        "type" : "exact",
        "value" : 10
    },
    "Manganeso":{
        "type" : "exact",
        "value" : 0.1
    },
    "Nitrato":{
        "type" : "exact",
        "value" : 10
    },
    "Coliformes totales": {
        "type" : "exact",
        "value" : 0
    }, 
    "Escherichia coli": {
        "type" : "exact",
        "value" : 0
    }
}