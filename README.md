# Proyecto de Transito de Ciudad de Buenos Aires

![Proyecto_de_Transito_de_Ciudad_de_Buenos_Aires](https://th.bing.com/th/id/R.9f5d364622231beb6608f946e178ac84?rik=%2fhyTZBWNGsaXhg&pid=ImgRaw&r=0)
---------

[![Python](https://img.shields.io/badge/Python-3.11+-dedede?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.99+-dedede?logo=fastapi&logoColor=white&labelColor=009688&style=for-the-badge)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-dedede?logo=mongodb&logoColor=white&style=for-the-badge&labelColor=47a248)](https://www.mongodb.com)
[![LucidChart](https://img.shields.io/badge/LucidChart-282c33?style=for-the-badge&logo=lucid&logoColor=white)](https://lucidchart.com)
[![PostMan](https://img.shields.io/badge/POSTMAN-FF6C37?style=for-the-badge&logo=postman&logoColor=fff)](https://www.postman.com)
[![Render](https://img.shields.io/badge/Render-000?style=for-the-badge&logo=render)](https://dashboard.render.com)

Este proyecto proporciona una serie de funcionalidades mucho más amigable con el usuario para realizar distintos análisis a la red de transporte de Ciudad Autónoma de Buenos Aires.

## Backend

```ASCCI
├── db
│  ├── lineaA.json
│  ├── lineaB.json
│  ├── lineaC.json
│  ├── lineaD.json
│  ├── lineaE.json
│  ├── lineaH.json
│  ├── __calls__.json
│  └── __data__.json
├── logs
│  └── .json
├── models
│  ├── estacion_subte.py
│  ├── linea_subte.py
│  └── movil_subte.py
├── routes
│  ├── API_subtes.py
│  ├── TransporteAPI.py
│  └── upload_info_db.py
├── schemas
│  └── db_client.py
└── main.py
```

En este directorio van a encontrar todo lo relacionado a la construcción, validación, modelado de datos, y posteo de los distintos endpoints que nos brinda el API del que se alimenta todo este proyecto.

[![API-TRANSPORTE](https://img.shields.io/badge/API--Transporte-FFEE19?style=for-the-badge)](https://api-transporte.buenosaires.gob.ar/console)

## Otros recursos

Diagrama del proyecto en LucidChart: [![LucidChart](https://img.shields.io/badge/LUCIDCHART-proyecto__caba-FE3?logo=lucid&style=for-the-badge&labelColor=282C33)](https://lucid.app/lucidchart/4a0a04b7-c881-40ce-b104-f4bdcd9c258e/edit?viewport_loc=154%2C486%2C1870%2C778%2C0_0&invitationId=inv_0e5c4899-2672-438b-a79c-3f6646036376)
