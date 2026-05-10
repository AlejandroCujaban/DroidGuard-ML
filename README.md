# Android Malware Consensus Predictor 🛡️🤖

Este proyecto implementa un modelo de **Machine Learning** capaz de predecir el veredicto de múltiples motores de antivirus basándose exclusivamente en el análisis estático de archivos APK.

## 🚀 Resumen del Proyecto
El sistema utiliza un clasificador multietiqueta para unificar los criterios de diversos proveedores de seguridad, logrando identificar patrones comunes de malware mediante permisos y estructuras de archivos.

* **Algoritmo:** Random Forest (MultiOutputClassifier).
* **Exactitud Global:** 90.62%.
* **Dataset:** Reportes JSON de VirusTotal almacenados en MongoDB.

## 🛠️ Tecnologías Utilizadas
* **Python:** Procesamiento y modelado.
* **MongoDB:** Almacenamiento de datos semiestructurados.
* **Scikit-Learn:** Implementación de IA.
* **Matplotlib/Seaborn:** Análisis exploratorio de datos.

## 📊 Hallazgos Clave
* Se identificó que el uso de **Random Forest** es óptimo para este dominio al ser invariante a la escala y manejar eficientemente datos desbalanceados.
* El filtrado hacia un "Grupo de Consenso" (motores como ESET, Sophos, Avira) elevó drásticamente la calidad predictiva.
* Motores de referencia como **ESET-NOD32** y **Sophos** alcanzaron una precisión del 100% en las pruebas.

## ⚙️ Instalación
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Asegurarse de tener una instancia de MongoDB corriendo con los datos de VirusTotal.

---
**Autor:** Oscar Alejandro Florez Cujaban.
