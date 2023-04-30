# FLACK || CS50w-Project02

> Proyecto inspirado de cs50w edición 2019 por Harvard.
> Flack[¹] 
### Tecnologías usadas.
- Python-Flask
- SocketIO-Flask
- JavaScript
- SASS
- CSS
- HTML

### Estructura del directorio.
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

## Dudas sobre ciertos funcionamientos.
### ¿Cómo funciona el cambio de chats? 

Al dar click en cualquier chat este primero es redirigido a la
ruta `/channel` en donde *"channel"* es una *variable*[³] dentro de
la ruta, de aquŕ sacamos el nombre del chat para poder obtener la información
necesaria.

Luego de que la página cargase en la nueva ruta, se activan las 
funciones de socket de `exitRoom` y `enterRoom` en simultáneo, para ya luego
dejar que el usuario pueda enviar mensajes y que estos se guarden 
correctamente.


### ¿Cómo funciona la redirección hacia un chat, luego de haber cerrado su ventana o pestaña?

Al cargar la pagina en `channels.js` obtenemos del servidor mediante Socket 
el nombre del canal previo antes de cerrarlo, junto con un estado de True o False,
dependiendo del estado cambiamos la ruta en el cliente en `window.location.pathname` 
colocandole el nombre del canal.

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
[²]:<https://linux.die.net/man/1/tree>
[³]:<https://flask.palletsprojects.com/en/2.2.x/quickstart/#variable-rules>
