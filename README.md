# FLACK || CS50w-Project02
> *Proyecto inspirado de cs50w edición 2019 por Harvard*,
> *[Flack][1]* 

----

#### TODO:
- [x] ~~Solucionar los bugs de la version de entrega.~~
- [ ] Implementar al menos 1 funcionalidad especial o toque personal.

----

### Tecnologías usadas.
- Flask
- SocketIO-Flask
- JavaScript
- SASS
- HTML&CSS

----

### Estructura del directorio.
```
📁
├── application.py
├── tools.py
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

----

### Dudas sobre ciertos funcionamientos.
> #### ¿Cómo funciona el cambio de chats?

Primero redirrecionamos con el servidor en [*`/<channel>`*][2] , luego en el cliente 
ejecutamos *`exitRoom`* y *`enterRoom`* simultanemente, saliendonos de cualquier
canal previo y entrando al actual, esto cada vez que carguemos la pagina.


> #### ¿Cómo funciona la redirección hacia un chat, luego de haber cerrado su ventana o pestaña?

Al cargar la pagina en *`channels.js`* obtenemos del servidor mediante Socket 
el nombre del canal previo antes de cerrarlo, junto con un estado de *`True`* o *`False`*,
dependiendo del estado cambiamos la ruta en el cliente en *`window.location.pathname`* 
colocandole el nombre del canal.

----

### Detalles

1) El toque personal no pude completarlo a tiempo o por lo menos
 desarrollar una buena parte del mismo. D:

2) Agregue un *`context_processor`* para siempre mostrar una lista de canales,
sin importar donde, pero la verdad no sé si sirva de mucho.

3) Pude haber hecho todo en una sola ruta, pero me compliqué con Socket, 
entonces me fui a por lo que más dominaba: *las rutas de Flask*. 

4) Es mi primera vez creando un chat en tiempo real y sin base de datos, 
hablando de ***BASE DE DATOS***, no recuerdo haber usado el almacenamiento 
del navegador/cliente, todos los datos son procesados en la memoria del servidor, 
usando variables globales como *`session`*, *`db_messages`* y *`channels`*.

[1]:<https://cs50.harvard.edu/extension/web/2019/fall/projects/2/>
[2]:<https://flask.palletsprojects.com/en/2.2.x/quickstart/#variable-rules>
