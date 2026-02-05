from io import BytesIO

from altair import Color

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, A4

class PDF:

    @staticmethod
    def generar_pdf_estetico(muestra, logo_usta_path, logo_empresa_path):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Logos proporcionales
        logo_usta = ImageReader(logo_usta_path)
        logo_empresa = ImageReader(logo_empresa_path)

        def dibujar_logo(img_reader, x, y, max_width, max_height):
            iw, ih = img_reader.getSize()
            ratio = min(max_width / iw, max_height / ih)
            new_w, new_h = iw * ratio, ih * ratio
            c.drawImage(img_reader, x, y, width=new_w, height=new_h, mask='auto')

        dibujar_logo(logo_usta, 50, height - 100, 100, 100)
        dibujar_logo(logo_empresa, width - 150, height - 100, 85, 85)

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 120, "Informe de Análisis de Muestra")

        y = height - 150
        c.setFont("Helvetica", 11)
        for k in ["Código", "Fecha", "Hora"]:
            if k in muestra:
                c.drawString(50, y, f"{k}: {muestra[k]}")
                y -= 20

        c.line(50, y, width - 50, y)
        y -= 20

        if muestra.get("Valores FQ"):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Parámetros físico-químicos:")
            y -= 18
            c.setFont("Helvetica", 11)
            for k, v in muestra["Valores FQ"].items():
                c.drawString(70, y, f"{k}: {v}")
                y -= 15

        y -= 10
        c.line(50, y, width - 50, y)
        y -= 20

        if muestra.get("Valores Micro"):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Parámetros microbiológicos:")
            y -= 18
            c.setFont("Helvetica", 11)
            for k, v in muestra["Valores Micro"].items():
                c.drawString(70, y, f"{k}: {v}")
                y -= 15

        # Marca de agua
        c.saveState()
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.2))
        c.drawCentredString(width / 2, 40, "Empresa de Aguas de Facatativá")
        c.restoreState()

        c.save()
        buffer.seek(0)
        return buffer 
    
    @staticmethod
    def generar_pdf_masivo(self, data):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Listas completas de parámetros (Aparecerán todos)
        PARAM_FQ = [
            "Temperatura","pH","Cloro residual libre","Alcalinidad total","Aluminio residual",
            "Calcio","Cloruros","Color aparente","Conductividad","Dureza total","Fosfato",
            "Hierro total","Magnesio","Nitrito","Sólidos disueltos totales","Sulfatos","Turbiedad",
            "Amonio","DQO","Dureza cálcica","Fenol","Fluoruro","Manganeso","Nitrato","Oxígeno disuelto"
        ]
        PARAM_MICRO = ["Coliformes totales", "Escherichia coli", "Mesófilos aerobios"]
        
        UNIDADES = {
            "Temperatura": "°C", "pH": "Unidades", "Cloro residual libre": "mg Cl2/L", "Alcalinidad total": "mg CaCO3/L",
            "Aluminio residual": "mg Al/L", "Calcio": "mg Ca/L", "Cloruros": "mg Cl/L", "Color aparente": "UPC",
            "Conductividad": "uS/cm", "Dureza total": "mg CaCO3/L", "Fosfato": "mg PO4/L", "Hierro total": "mg Fe/L",
            "Magnesio": "mg Mg/L", "Nitrito": "mg NO2/L", "Sólidos disueltos totales": "mg/L", "Sulfatos": "mg SO4/L",
            "Turbiedad": "UNT", "Amonio": "mg NH4/L", "DQO": "mg O2/L", "Dureza cálcica": "mg CaCO3/L",
            "Fenol": "mg C6H5OH/L", "Fluoruro": "mg F/L", "Manganeso": "mg Mn/L", "Nitrato": "mg NO3/L",
            "Oxígeno disuelto": "mg OD/L", "Coliformes totales": "NMP/100mL", "Escherichia coli": "NMP/100mL", "Mesófilos aerobios": "UFC/mL"
        }

        for i, muestra in enumerate(data):
            if i > 0: p.showPage()
            y = self.draw_header_pdf(p, width, height)
            self.draw_footer_pdf(p, width, height)

            # 1. INFORMACIÓN DE RECEPCIÓN
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "1. INFORMACIÓN DE RECEPCIÓN Y MUESTREO")
            y -= 20
            p.setFont("Helvetica", 9); p.setFillColor(Color(0, 0, 0))
            
            col1, col2 = 60, 320
            datos = [
                (f"Código: {muestra.get('Código', 'N/A')}", f"Fuente: {muestra.get('Fuente', 'N/A')}"),
                (f"Fecha Muestra: {muestra.get('Fecha', 'N/A')}", f"Hora Muestra: {muestra.get('Hora', 'N/A')}"),
                (f"Fecha Recepción: {muestra.get('Fecha Recepción', 'N/A')}", f"Recepcionista: {muestra.get('Recepcionó', 'N/A')}"),
                (f"Temp. Recepción: {muestra.get('Temperatura Recepción', '0')} °C", f"Tipo de Agua: {muestra.get('Tipo Agua', 'N/A')}")
            ]
            for d1, d2 in datos:
                p.drawString(col1, y, d1); p.drawString(col2, y, d2); y -= 14

            # 2. ANÁLISIS FÍSICO-QUÍMICO (Todos los campos)
            y -= 10
            p.setFont("Helvetica-Bold", 12); p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "2. ANÁLISIS FÍSICO-QUÍMICO")
            y -= 18
            p.setFont("Helvetica-Bold", 9); p.setFillColor(Color(0, 0, 0))
            p.drawString(60, y, "Parámetro"); p.drawString(300, y, "Resultado"); p.drawString(450, y, "Unidad")
            p.line(45, y-2, width-45, y-2); y -= 15
            
            res_fq = muestra.get("Valores FQ", {})
            for param in PARAM_FQ:
                y = self.check_y(width, height, y, p)
                p.setFont("Helvetica", 9)
                p.drawString(60, y, param)
                p.drawString(300, y, str(res_fq.get(param, "0.00")))
                self.draw_unit_safely(p, 450, y, UNIDADES.get(param, ""))
                y -= 13

            # 3. ANÁLISIS MICROBIOLÓGICO
            y -= 15
            y = self.check_y(width, height, y, p)
            p.setFont("Helvetica-Bold", 12); p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "3. ANÁLISIS MICROBIOLÓGICO")
            y -= 18
            p.line(45, y+10, width-45, y+10)
            
            res_micro = muestra.get("Valores Micro", {})
            for param in PARAM_MICRO:
                y = self.check_y(width, height, y, p)
                p.setFont("Helvetica", 9)
                p.drawString(60, y, param)
                p.drawString(300, y, str(res_micro.get(param, "0.00")))
                self.draw_unit_safely(p, 450, y, UNIDADES.get(param, ""))
                y -= 13

        p.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def check_y(self, width, height, current_y, p_obj):
            if current_y < 80:
                p_obj.showPage()
                self.draw_footer_pdf(p_obj, width, height)
                return self.draw_header_pdf(p_obj, width, height)
            return current_y
    
    def draw_header_pdf(p, width, height):
        #Dibuja el encabezado. Ajustado para que el logo USTA no se vea corrido.
        y_start = height - 40 
        # Logo Empresa (Izquierda)
        try:
            logo_empresa = ImageReader("images/LOGO.png")
            p.drawImage(logo_empresa, 50, y_start - 45, width=65, height=65, preserveAspectRatio=True, mask='auto')
        except: pass
        
        # Logo USTA (Derecha) - Coordenadas corregidas
        try:
            logo_usta = ImageReader("images/LOGO USTA.png")
            p.drawImage(logo_usta, width - 125, y_start - 45, width=80, height=80, preserveAspectRatio=True, mask='auto')
        except: pass
        
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(Color(0, 0.34, 0.63))
        p.drawCentredString(width / 2, y_start - 25, "UNIVERSIDAD SANTO TOMÁS")
        p.setFont("Helvetica-Bold", 11)
        p.drawCentredString(width / 2, y_start - 45, "SISTEMA DE GESTIÓN DE LABORATORIO")
        p.setStrokeColor(Color(0, 0.34, 0.63))
        p.line(40, height - 100, width - 40, height - 100)
        return height - 125 

    def draw_footer_pdf(p, width, height):
        footer_y = 45 
        p.setFillColor(Color(0.95, 0.95, 0.95)) 
        p.rect(0, 0, width, footer_y + 10, fill=1, stroke=0)
        p.setFillColor(Color(0, 0, 0))
        p.setFont("Helvetica-Bold", 8)
        p.drawString(45, footer_y, "Laboratorio de Calidad del Agua")
        p.setFont("Helvetica", 7)
        p.drawString(45, footer_y - 10, "Universidad Santo Tomás – Facultad de Ingeniería Ambiental")
        p.drawString(45, footer_y - 20, "📍 Bogotá D.C. | ☎️ +57 314 367 9332 | ✉️ km@usantotomas.edu.co")

    def draw_unit_safely(p, x, y, unit_text):
        """Dibuja unidades como Cl2 o CaCO3 sin usar caracteres unicode problemáticos."""
        p.setFont("Helvetica", 9)
        # Diccionario de reemplazos manuales para subíndices
        if "Cl2" in unit_text:
            p.drawString(x, y, "mg Cl")
            p.setFont("Helvetica", 6); p.drawString(x + 25, y - 2, "2"); p.setFont("Helvetica", 9)
            p.drawString(x + 30, y, "/L")
        elif "CaCO3" in unit_text:
            p.drawString(x, y, "mg CaCO")
            p.setFont("Helvetica", 6); p.drawString(x + 38, y - 2, "3"); p.setFont("Helvetica", 9)
            p.drawString(x + 43, y, "/L")
        elif "PO4" in unit_text:
            p.drawString(x, y, "mg PO")
            p.setFont("Helvetica", 6); p.drawString(x + 28, y - 2, "4"); p.setFont("Helvetica", 9)
            p.drawString(x + 33, y, "/L")
        else:
            p.drawString(x, y, unit_text)