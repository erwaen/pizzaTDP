# pizzaTDP


# Requisitos
* Python 3.6 para adelante
* Sistema operativo Unix-like

# Instalacion


# Endpoints

|  Path          |     Query    |    Method | Description | 
| -------------  | -------------| --------- | --------- |
| /logear-jwt  | username: str, password: str   |    <b style="color:Fuchsia;">POST</b>    |  Login para autenticacion con JWT, retorna los tokens access_token y refresh_token.   |
| /signup  | body(JSON) {<br>"username": "",<br>password": ""<br>"is_staff": true,<br>"is_superuser": false"<br>}    |    <b style="color:Fuchsia;">POST</b>    |  Para crear un nuevo usuario y asignarle un rol.  |
| /pizzas/    |    | <b style="color:LawnGreen;">GET</b>       | Retorna todas las las pizzas activas con su nombre, precio y numero de ingredientes que tiene. Si el user es staff o superuser entonces tambien retorna las no activas. |
| /pizzas/{pizzaID}    |  pizzaID: int  | <b style="color:LawnGreen;">GET</b>       | Retorna los detalles de la pizza mostrando el nombre, precio, si esta activo o no y sus ingredientes |
| /pizzas/    | bodyExample(JSON){<br>"nombre": "brasilera",<br> "precio": 10000,<br>"is_active": true<br>}   | <b style="color:Fuchsia;">POST</b>       | Crea una nueva pizza dado en el body su nombre, precio y si va a estar activa o no. |
| /pizzas/{pizzaID}    |  nombre: str<br>precio: str<br>is_active: bool  | <b style="color:gray;">PATCH </b>       | Modifica la pizza con id pizzaID con los valores que se le pasa como parametros |
| /ingredientes/    |  bodyExample(JSON){<br>"nombre": "choclo",<br>"categoria" : "basico"/"premium"<br>}  | <b style="color:Fuchsia;">POST</b>       | Para crear un nuevo ingrediente pasandole el body el nombre y la categoria (la categoria se controla que sea solo "basico" o "premium") |
| /ingredientes/{ingredienteID}    |  bodyExample(JSON){<br>"nombre": "pinha",<br>"categoria" : "basico"/"premium"<br>}  | <b style="color:gray;">PATCH </b>      | Modifica el ingrediente con id ingredienteID con los valores que se le pasa en el body |
| /ingredientes/{ingredienteID/   |  | <b style="color:red;">DELETE</b>       | Elimina un ingrediente de la base de datos y antes controla que ninguna pizza use ese ingrediente |
| /pizza-ingrediente/   | p_id: int<br>ingr_id: int |  <b style="color:Fuchsia;">POST</b>       | Agrega el ingrediente con id ingr_id a la pizza con id p_id |
| /pizza-ingrediente/{p_id}/{ingr_id}   |  |   <b style="color:red;">DELETE</b>      | Elimina un ingrediente con id ingr_id de la pizza con id p_id  |