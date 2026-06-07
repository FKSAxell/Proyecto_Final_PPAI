# 🎓 Análisis de Factores de Rendimiento Académico Estudiantil

Proyecto Final Integrador — **Paradigmas de Programación para Inteligencia Artificial y Análisis de Datos**  
Maestría en Inteligencia Artificial y Ciencia de Datos

---

## Descripción

Aplicación interactiva desarrollada con **Streamlit** y **Python** que permite cargar, explorar, analizar y visualizar el dataset *Student Performance Factors*, identificando los factores con mayor incidencia en el rendimiento académico de 6 607 estudiantes.

## Dataset

| Atributo | Detalle |
|---|---|
| Fuente | [Kaggle — Student Performance Factors](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) |
| Registros | 6 607 |
| Variables | 20 (7 numéricas · 13 categóricas) |
| Variable objetivo | `Exam_Score` (puntaje de examen) |

## Estructura del proyecto

```
Proyecto_Final_PPAI/
├── app.py                        # Punto de entrada — navegación con st.navigation
├── utils.py                      # Constantes, traducciones y funciones auxiliares
├── rutas/
│   ├── inicio.py                 # Carga del dataset y métricas globales
│   ├── exploracion.py            # Estructura, estadísticas y valores nulos
│   ├── univariado.py             # Distribuciones por variable (histograma, boxplot, barras, pie)
│   ├── bivariado.py              # Correlaciones y relaciones entre variables
│   ├── factores.py               # Factores clave del rendimiento
│   └── conclusiones.py           # Hallazgos, recomendaciones y referencias
├── data/
│   └── StudentPerformanceFactors.csv
├── requirements.txt
└── README.md
```

## Instalación local

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd Proyecto_PPAI

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run app.py
```

La app queda disponible en `http://localhost:8501`

## Dependencias principales

| Librería | Uso |
|---|---|
| `streamlit >= 1.36` | Interfaz web interactiva |
| `pandas` | Manipulación del dataset |
| `plotly` | Gráficos interactivos |
| `seaborn / matplotlib` | Heatmap de correlaciones |
| `statsmodels` | Líneas de tendencia OLS |

## Hallazgos principales

1. **Asistencia (r = 0.58)** — predictor más fuerte del puntaje de examen
2. **Horas de estudio (r = 0.45)** — segundo predictor; ambas variables son complementarias
3. **Factores de contexto** — ninguna variable categórica supera 2 puntos de diferencia entre grupos

## Autores

**Kevin Axell Concha Regatto**  
**Rogwi Alexis Cajas Correa**
