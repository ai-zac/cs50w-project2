# FLACK || CS50w-Project02

> Proyecto inspirado de cs50w edición 2018 por Harvard
> Flack[¹] 

> *El link es de la edición 2019, no encontre la del 2018*


---


### Tecnologías usadas
- Python-Flask
- SocketIO-Flask
- JavaScript
- AJAX
- SASS
- CSS
- HTML


### Directorio
> No mucho que agregar, solo un orden clásico de directorios para 
> Flask. 

> **P.D.** Utilice *tree*[²] para sacar este esquema en ASCII 
```
📁
├── application.py
├── login_required.py
├── README.md
├── requirements.txt
├── templates
│   ├── channel.html
│   ├── index.html
│   └── login.html
└── static
    ├── css
    │   ├── index.css
    │   ├── index.css.map
    │   ├── index.scss
    │   ├── login.css
    │   ├── login.css.map
    │   └── login.scss
    └── js
        ├── channels.js
        └── messages.js
```

## Ahora algunas preguntas sobre ciertos funcionamientos

### ¿Cómo funciona el cambio de chats? 

Al dar click en cualquier chat este primero es redirigido a la
ruta `/channel` en donde *"channel"* es una *variable*[³] dentro de
la ruta, de aquŕ sacamos el nombre del chat para poder obtener la información
necesaria.

Luego de que la página cargase en la nueva ruta, se activan las 
funciones de socket de `exitRoom` y `enterRoom` en simultáneo, para ya luego
dejar que el usuario pueda enviar mensajes y que estos se guarden 
correctamente.


### ¿Cómo funciona la redirección al chat previo?

> Con lo del ***chat previo*** me refiero al chat en el que estaba el 
> usuario antes de cerrar la ventana o pestaña en donde estaba Flack 
> , este al volver abrir la aplicación debe ser redirigido a ese chat.

En los scripts esta `channels.js - línea:12`, se detecta si la ruta es `/`, 
de ser así usando AJAX se busca el chat previo, para luego ser redirigido 
hacia allí, esta información se guarda en una variable de Flask llamada
`session`.


----


### Detalles

> Esto no es el toque personal, no pude completarlo a tiempo o por lo menos
> desarrollar una buena parte del mismo.

1) Agregue un `context_processor` para siempre mostrar una lista de canales,
no importe donde, pero la verdad no sé si sirva de mucho.

2) Pude haber hecho todo en una sola ruta, pero me compliqué con Socket, 
entonces me fui a por lo seguro que son las rutas de Flask. 

3) Es mi primera vez creando un chat en tiempo real y sin base de datos, 
hablando de ***BASE DE DATOS***, no recuerdo haber usado el almacenamiento 
del navegador, todos los datos son procesados en la memoria del servidor, 
en variables como `session`, `session_tmp`, `messages` y `chnls`.

[¹]:<https://cs50.harvard.edu/extension/web/2019/fall/projects/2/>
[²]: <https://linux.die.net/man/1/tree>
[³]: <https://flask.palletsprojects.com/en/2.2.x/quickstart/#variable-rules>
