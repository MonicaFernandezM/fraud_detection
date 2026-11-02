# Fraud Detection and Cost Optimization

## Description 
Este proyecto consiste en el análisis de un dataset de fraude con el objetivo de identificar patrones relevantes y cuantificar el impacto económico del fraude en un negocio.

A diferencia de un enfoque tradicional basado en métricas técnicas, este proyecto se centra en:

- ¿Dónde se concentra el fraude?
- ¿Cuánto dinero se está perdiendo?
- ¿Cómo optimizar decisiones para reducir ese coste?

## Tabla de Contenidos
- [Descripción](#descripción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Dataset](#dataset)
- [Preguntas de Investigación](#preguntas-de-investigación)
- [Análisis](#análisis)
- [Resultados](#resultados)
- [Conclusiones](#conclusiones)
- [Dashboard](#dashboard)
- [Contribución](#contribución)
- [Autor](#autor)

## Instalación

1. Clonar el repositorio:
```bash
   git clone [https://github.com/MonicaFernandezM/fraud_detection](https://github.com/MonicaFernandezM/fraud_detection)
```

2. Instalar dependencias:
pip install -r requirements.txt

3. Ejecutar el dashboard:
streamlit run app7.py

## Uso

- Seleccionar filtros (producto, tipo de tarjeta)
- Ajustar el **threshold del modelo**
- Analizar:
    - Fraude detectado vs no detectado
    - Coste económico
    - Segmentos de mayor riesgo

El dashboard está diseñado para facilitar la **toma de decisiones basada en impacto económico**.

## Dataset

El análisis integra datos de transacciones obtenidos de la competición de Kaggle [IEEE-Fraud-Detection](https://www.kaggle.com/competitions/ieee-fraud-detection). Los datos fueron limpiados y procesados previamente.

Variables clave utilizadas:

- Tipo de producto (ProductCD)
- Tipo de tarjeta (card4)
- Probabilidad de fraude (y_proba)
- Variable objetivo (isFraud)

Los datos han sido previamente limpiados y procesados para su análisis.

## Preguntas de Investigación

- ¿Dónde se concentra el fraude?
- ¿Qué productos presentan mayor riesgo?
- ¿Qué tipo de tarjeta tiene mayor tasa de fraude?
- ¿Cuánto fraude no se está detectando?
- ¿Cuál es el impacto económico total?
- ¿Cuál es el threshold óptimo para minimizar pérdidas?

## Análisis realizado

El proyecto incluye:

- Limpieza y transformación de datos
- Modelado de fraude mediante Machine Learning
- Cálculo de métricas (Precision, Recall)
- Definición de función de coste:
    - Fraude no detectado → pérdida directa
    - Falsas alertas → coste operativo
- Optimización del threshold basada en minimización de coste
- Análisis por segmentos (producto y tarjeta)

## Resultados 

##### Impacto económico del fraude:

El análisis muestra que una parte significativa del fraude no se detecta, generando pérdidas directas para el negocio.

Además, las falsas alertas generan un coste operativo adicional.

Se define el coste como:
Coste total = (FN * 100€) + (FP * 5€)

##### Optimización del threshold:

El threshold estándar no es óptimo desde el punto de vista de negocio.

Ajustar el umbral de decisión frente al estándar de Machine Learning permite:
- Reducir drásticamente el fraude no detectado.
- Equilibrar el volumen de falsas alertas.
- Minimizar el coste económico total de la operación.

##### Segmentos de mayor riesgo:

El análisis identifica:

- Productos con mayor tasa de fraude  
- Tipos de tarjeta más vulnerables  

Esto permite priorizar acciones de prevención.

##### Insight clave:

El mejor modelo no es el que tiene mejor AUC,  
sino el que **minimiza el coste económico**.

## Conclusiones
- El mejor modelo no es el que maximiza el AUC, sino el que se alinea con la estrategia financiera del negocio minimizando costes.
- La optimización del threshold basada en costes operativos y pérdidas directas aporta un valor empresarial muy superior a los umbrales de probabilidad por defecto (0.5).
- La segmentación por producto y tipo de tarjeta permite enfocar los recursos de control antifraude de manera mucho más eficiente.

## Dashboard

### Resultados del modelo
![Confusion Matrix](images/confusion_matrix.png)

### Fraude por producto
![Fraud by Product](images/fraud_product.png)

### Fraude por tipo de tarjeta
![Fraud by Card](images/fraud_card.png)

## Contribución 

Las contribuciones son bienvenidas.

Si deseas mejorar el análisis o añadir funcionalidades:

1. Haz un fork del repositorio  
2. Crea una nueva rama (git checkout -b feature/mejora)
3. Realiza tus cambios y haz commit (git commit -m 'Añadir mejora')  
4. Abre un Pull Request  

## Autor

Mónica Fernández  
[linkedin](www.linkedin.com/in/monicamfm)
