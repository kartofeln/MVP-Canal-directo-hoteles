# 🎨 Guía de Diseño Figma - LinkedIn Post Sector Turístico

## 📋 **Información del Proyecto Figma**

### **Dimensiones del Diseño:**
- **Frame Principal**: 1200 x 628 px (Formato LinkedIn)
- **Frames Secundarios**: 1080 x 1080 px (Carrusel)
- **Resolución**: 72 DPI
- **Formato de Exportación**: PNG

---

## 🎯 **Estructura del Diseño**

### **Frame 1: Post Principal (1200x628px)**
```
┌─────────────────────────────────────┐
│  🌍 Sector Turístico                │ ← Header con gradiente azul
│  Datos actualizados de turismo...   │
├─────────────────────────────────────┤
│  📊 Julio 2025                      │ ← Highlight principal
│  Análisis del turismo interno...    │
├─────────────────────────────────────┤
│  🏖️ 🏔️ 🏛️ 🍽️                      │ ← Grid de 4 tarjetas
│  Destinos Turismo Turismo Turismo   │
│  Costeros Rural Cultural Gastronóm. │
├─────────────────────────────────────┤
│  💡 Insights Clave:                 │ ← Caja de insights
│  • Recuperación sostenida...        │
│  • Nuevas tendencias...             │
│  • Impacto de la digitalización...  │
├─────────────────────────────────────┤
│  #TurismoEspaña #SectorTurístico... │ ← Hashtags + CTA
│  📈 Ver análisis completo           │
└─────────────────────────────────────┘
```

---

## 🎨 **Paleta de Colores**

### **Colores Principales:**
- **Azul LinkedIn**: `#0077b5`
- **Azul Claro**: `#00a0dc`
- **Verde CTA**: `#28a745`
- **Verde Claro**: `#20c997`

### **Gradientes:**
- **Header**: `linear-gradient(135deg, #0077b5 0%, #00a0dc 100%)`
- **Highlight**: `linear-gradient(135deg, #f093fb 0%, #f5576c 100%)`
- **CTA**: `linear-gradient(135deg, #28a745 0%, #20c997 100%)`

### **Colores de Fondo:**
- **Principal**: `#ffffff`
- **Tarjetas**: `#f8f9fa`
- **Insights**: `#e3f2fd`
- **Footer**: `#f8f9fa`

---

## 📝 **Contenido del Post**

### **Texto Principal:**
```
🌍 Nuevos datos del sector turístico español revelan tendencias prometedoras

Los datos más recientes del Instituto de Estudios Turísticos (IET) muestran una recuperación sostenida del turismo doméstico en España durante junio-julio 2025.

📈 Hallazgos clave:
• Recuperación del 15% en viajes nacionales vs 2024
• Aumento del turismo rural y de naturaleza
• Mayor preferencia por destinos menos masificados
• Digitalización acelerada en la planificación de viajes

🏖️ Destinos más populares:
- Costa del Sol
- Islas Baleares
- País Vasco
- Galicia

💡 Insights para el sector:
La transformación digital está redefiniendo cómo los turistas planifican y experimentan sus viajes. Las empresas del sector que se adapten a estas nuevas preferencias tendrán una ventaja competitiva significativa.

🔗 Datos completos: [API SEGITTUR]

#TurismoEspaña #SectorTurístico #DatosTurismo #SEGITTUR #TurismoDoméstico #AnálisisTurístico #RecuperaciónTurística #DigitalizaciónTurismo
```

---

## 🔧 **Pasos para Crear en Figma**

### **Paso 1: Configuración Inicial**
1. Crear nuevo proyecto en Figma
2. Crear frame de 1200x628px
3. Configurar grid: 12 columnas, 8 filas
4. Añadir guías de seguridad (márgenes de 40px)

### **Paso 2: Header**
1. Crear rectángulo con gradiente azul
2. Añadir texto "🌍 Sector Turístico" (Inter Bold, 48px)
3. Añadir subtítulo (Inter Regular, 24px)
4. Centrar elementos

### **Paso 3: Highlight Principal**
1. Crear rectángulo con gradiente rosa/púrpura
2. Añadir "📊 Julio 2025" (Inter Bold, 36px)
3. Añadir descripción (Inter Regular, 20px)
4. Aplicar border-radius de 12px

### **Paso 4: Grid de Tarjetas**
1. Crear 4 rectángulos de 280x120px
2. Añadir iconos emoji (48px)
3. Añadir texto descriptivo (Inter Medium, 16px)
4. Aplicar sombra sutil

### **Paso 5: Caja de Insights**
1. Crear rectángulo con fondo azul claro
2. Añadir título "💡 Insights Clave:"
3. Crear lista con bullets
4. Usar Inter Regular, 18px

### **Paso 6: Footer**
1. Crear sección con hashtags
2. Añadir botón CTA con gradiente verde
3. Usar Inter Medium para hashtags
4. Usar Inter Bold para CTA

---

## 📱 **Versiones Móviles**

### **Frame 2: Carrusel (1080x1080px)**
```
┌─────────────────┐
│  🌍             │
│  Sector         │
│  Turístico      │
├─────────────────┤
│  📊 Julio 2025  │
│  +15% vs 2024   │
├─────────────────┤
│  🏖️ Costa del   │
│     Sol         │
├─────────────────┤
│  🏔️ Turismo     │
│     Rural       │
├─────────────────┤
│  📱 Digitalización│
│     Acelerada   │
└─────────────────┘
```

---

## 🎯 **Elementos Interactivos**

### **Hover States:**
- **Tarjetas**: Elevación + 2px
- **CTA**: Escala 1.05
- **Hashtags**: Opacidad 0.8

### **Animaciones (si aplica):**
- **Entrada**: Fade in desde abajo
- **Hover**: Transición suave 0.3s
- **Carga**: Stagger animation

---

## 📊 **Tipografía**

### **Jerarquía:**
- **H1**: Inter Bold, 48px
- **H2**: Inter Bold, 36px
- **H3**: Inter Bold, 24px
- **Body**: Inter Regular, 18px
- **Caption**: Inter Medium, 16px
- **CTA**: Inter Bold, 20px

### **Espaciado:**
- **Line-height**: 1.4
- **Letter-spacing**: 0.5px
- **Paragraph spacing**: 24px

---

## 🚀 **Exportación**

### **Formatos:**
- **PNG**: Para LinkedIn
- **JPG**: Para compresión
- **SVG**: Para escalabilidad

### **Resoluciones:**
- **1x**: 1200x628px
- **2x**: 2400x1256px (para pantallas retina)

---

## 💡 **Consejos de Diseño**

### **Accesibilidad:**
- Contraste mínimo 4.5:1
- Tamaño de texto mínimo 16px
- Iconos con texto alternativo

### **Branding:**
- Mantener consistencia con colores corporativos
- Usar logo en esquina si aplica
- Incluir marca de agua sutil

### **Optimización:**
- Comprimir imágenes antes de exportar
- Usar colores web-safe
- Optimizar para carga rápida

---

## 📋 **Checklist Final**

- [ ] Dimensiones correctas (1200x628px)
- [ ] Colores de marca aplicados
- [ ] Tipografía consistente
- [ ] Espaciado uniforme
- [ ] Elementos alineados
- [ ] Contraste adecuado
- [ ] Texto legible
- [ ] Exportación optimizada
- [ ] Versión móvil creada
- [ ] Archivos organizados

---

**¡Con esta guía tendrás un diseño profesional y listo para LinkedIn!** 🎉





