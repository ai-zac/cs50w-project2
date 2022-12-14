#  FLASK || CS50w-Project02

> Projecto inspirado de cs50w edicion 2018 por Harvard
> Flack[¹] 

> *El link es de la edicion 2019, no encontre la del 2018*


---


### Tecnologias usadas
- Python-Flask
- SocketIO-Flask
- JavaScript
- AJAX
- SASS
- CSS
- HTML


### Directorio
> No mucho que agregar, solo un orden clasico de directorios para 
> Flask. 

> **P.D.** Utilice *tree*[²] para sacar este esquema en ascii 
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

### ¿Como funciona el cambio de chats? 

Al dar click en cualquier chat este primero es redirijido a la
ruta `/channel` en donde *"channel"* es una *variable*[³] dentro de
la ruta, de aqui sacamos el nombre del chat para poder obtener la informacion
necesaria.

Luego de que la pagina cargase en la nueva ruta, se activan las 
funciones de socket de `exitRoom` y `enterRoom` en simultaneo, para ya luego
dejar que el usuario pueda enviar mensajes y que estos se guarden 
correctamente.


### ¿Como funciona la redirrecion al chat previo?

> Con lo del ***chat previo*** me refiero al chat en el que estaba el 
> usuario antes de cerrar la ventana o pestaña en donde estaba Flack 
> , este al volver abrir la aplicacion debe ser redirijido a ese chat.

En los scripts esta `channels.js - linea:12`, se detecta si la ruta es `/`, 
de ser asi usando AJAX se busca el chat previo, para luego redirijirlo 
hacia alli, esta informacion se guarda en una variable de Flask llamada
`session`.


----


### Detalles

> Esto no es el toque personal, no pude completarlo a tiempo o por lo menos
> desarrollar una buena parte del mismo.

1) Agregue un `context_processor` para siempre mostrar una lista de canales,
no importe donde, pero la verdad no se si sirva de mucho.

2) Pude haber hecho todo en una sola ruta, pero me complique con Socket, 
entonces me fui a por lo seguro que son las rutas de Flask. 

3) Es mi primera vez creando un chat en tiempo real y sin base de datos, 
hablando de ***BASE DE DATOS***, no recuerdo haber usado el almacenamiento 
del navegador, todos los datos son procesados en la memoria del servidor, 
en variables como `session`, `session_tmp`, `messages` y `chnls`.

[¹]:<https://cs50.harvard.edu/extension/web/2019/fall/projects/2/>
[²]: <https://linux.die.net/man/1/tree>
[³]: <https://flask.palletsprojects.com/en/2.2.x/quickstart/#variable-rules>
