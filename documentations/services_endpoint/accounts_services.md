# Documentation of services app Accounts
## Login
Grants access to a user to start in app android o io

* Url

  http://127.0.0.1:8080/login/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
 {
  "username":"soulrac5",
  "password":"carlos123"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
     "username": "soulrac5",
     "id": 5,
     "token": "c57f8675157921a3318725d2bd32a042cf721db2",
     "last_login": "2018-02-28T00:43:46Z"
   }
   ```  
* Error Response:
  * code: 400
  
  when user does not exist
   ```javascript
   {
     "detail": "El usuario no existe en el sistema"
   }
   ``` 
  or

  * code: 400
  
  when the password dont match
  ```javascript
  {
    "detail": "Contraseña invalida, porfavor escriba correctamente su contraseña"
  }
  ```
  or

  * code: 400
  
  when the user account is inactive
  ```javascript
  {
    "detail": "Cuenta inactiva, su cuenta esta bloqueada"
  }
  ```
* Notes:

 **None**
 ___
 
 ## Logout
Logout the user for app and io

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/logout/

* Method

  **POST**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
   {
     "detail": "Te has desconectado del sistema"
   }
   ```  
* Error Response:
  * code: 401
   ```javascript
   {
     "detail": "Token inválido."
   }
   ``` 
* Notes:
 
  **None**
  ___
  
## Countrys
Get all country in the work

* Url

  http://127.0.0.1:8080/countrys/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
   {
     [
      {
          "id": 1,
          "code": "AF",
          "name": "Afghanistan"
      },
      {
          "id": 2,
          "code": "AL",
          "name": "Albania"
      },
      ...
     ]
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
    {
       "detail":"error"
    }
   ``` 
* Notes:
 
  **None**
___

## Terms of Conditions 
Get the term of conditions 

* Url

  http://127.0.0.1:8080/terms-conditions/

* Method

  **GET**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
   {
      "title": "terminos de weedmatch",
      "id": 1,
      "description": "l pasaje estándar Lorem Ipsum"   
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail":"error"
   }
   ``` 
* Notes:
 
  **None**
___

## Forgot password
service to send a request to recover the password for user

* Url

  http://127.0.0.1:8080/forgot-password/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
 {
    "email":"carlos@gmail.com"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
     "detail": "el correo se ha enviado con exito"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "el correo no esta registrado en el sistema"
   }
   ``` 
  or

  * code: 500
  ```javascript
  {
    'detail': 'Problemas del servidor no se ha podido realizar la peticion'
  }
  ```
* Notes:
 
  **None**
___


## Recover Password
service to send a request with the code and the new password obtained in the mail of user 

* Url

  http://127.0.0.1:8080/recover-password/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
 {
    "code":"VJ8BXYAH527G47BBXXUE",
    "password":"carlos1234"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
     'detail': 'La contraseña se ha cambiado con exito' 
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "Código que enviaste no coinciden con el registrado en tu cuenta"
   }
   ``` 
* Notes:
 
  **None**
___

## Profile User Service 
Show all information for the user 

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/profile/

  or 

  http://127.0.0.1:8080/profile/id/

  **id** user id
* Method

  **GET**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
       {
        "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
        "sex": "Mujer",
        "description": "",
        "email": "luisanaolivero2@hotmail.com",
        "credit_card": [
            {
                "number_card": "9864",
                "last_name": "olivero",
                "id": 2,
                "month": "02",
                "type_card": "visa",
                "year": "22",
                "first_name": "luisana"
            }
        ],
        "profile_images": [
            {
                "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png",
                "id": 3
            },
            {
                "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
                "id": 4
            }
        ],
        "first_name": "luisana",
        "match_sex": "Other",
        "username": "luisagtx",
        "country": {
            "id": 222,
            "code": "VE",
            "name": "Venezuela"
        },
        "id": 7,
        "age": 23,
        "direction": "Barrio 18 De Octubre, Maracaibo 4002, Zulia, Venezuela"
    }
   ```  
* Error Response:
  * code: 400
  ```javascript
  {
    "detail":"Token Invalido."
  }
  ```
* Notes:
 
  **None**
___

## Profile User Service
Update data of user

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/profile/id/

  **id** the user
* Method

  **PUT**

* Url Params

  **None**

* Data Params
 ```javascript
 {
    "username": "luisagtx",
	  "first_name": "luisana",
	  "direction": "Barrio 18 De Octubre",
	  "country": "222",
	  "description": "hola soy nueva",
	  "match_sex": "Mujer",
	  "sex": "Mujer"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
      "profile_images": [
        {
            "id": 3,
            "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png"
        },
        {
            "id": 4,
            "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg"
        }
    ],
    "description": "hola soy nuev en weedmatch me gusta la hierba brava :)",
    "direction": "Barrio 18 De Octubre, Maracaibo 4002, Zulia, Venezuela",
    "age": 23,
    "email": "luisanaolivero2@hotmail.com",
    "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
    "match_sex": "Mujer",
    "detail": "Tu información personal ha sido editada con exito",
    "credit_card": [
        {
            "number_card": "9864",
            "id": 2,
            "type_card": "visa",
            "first_name": "luisana",
            "year": "22",
            "month": "02",
            "last_name": "olivero"
        }
    ],
    "country": {
        "id": 222,
        "code": "VE",
        "name": "Venezuela"
    },
    "id_user": 7,
    "first_name": "luisana",
    "username": "luisagtx",
    "sex": "Mujer"
   }
   ```  
* Error Response:

  username exist

  * code: 400
   ```javascript
   {
     "detail": {
        "username": "El nombre de usuario existe, porfavor escriba otro nombre de usuario"
    }
   }
   ``` 
  or

  country no exist
  * code: 400
  ```javascript
  {
     "detail": {
        "country": "el pais no esta registrado en el sistema"
    }
  }
  ```
  or

  username empty
  * code: 400
  ```javascript
  {
     "detail": {
        "username": [
            "empty values not allowed",
            "min length is 6"
        ]
    }
  }
* Notes:
 
  **None**
___

## Profile User Service
change password in profile user

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/id/change-password/

  **id** user id
* Method

  **PUT**

* Url Params

  **None**

* Data Params
 ```javascript
 {
  "old_password":"carlos12",
  "new_password":"carlos123"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
     'detail': 'Su contraseña ha sido cambiada exitosamente',
     "last_login": "2018-03-16T13:09:07.907753Z",
     "token": "50184cf335e82e029bf13ded03090830d5b083f0",
     "id": 5,
     "username": "soulrac5"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "La contraseña ingresada no coincide con tu actual contraseña"
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
    "detail": "La contraseña debe tener caracteres y numeros"
  }
  ```
* Notes:
 
  **None**
___

## Profile User Service
upload image to profile user

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/profile/id/upload-image/

  **id** user id
* Method

  **POST**

* Url Params

  **None**

* Data Params
 
  Form Data
  * image

* Success Response:
   * code: 200
    ```javascript
   {
     "profile_images": [
        {
            "id": 3,
            "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png"
        },
        {
            "id": 4,
            "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg"
        }
    ],
    "description": "hola soy nuev en weedmatch me gusta la hierba brava :)",
    "direction": "Barrio 18 De Octubre, Maracaibo 4002, Zulia, Venezuela",
    "age": 23,
    "email": "luisanaolivero2@hotmail.com",
    "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
    "match_sex": "Mujer",
    "detail": "Has subido una imagen a tu perfil exitosamente",
    "credit_card": [
        {
            "number_card": "9864",
            "id": 2,
            "type_card": "visa",
            "first_name": "luisana",
            "year": "22",
            "month": "02",
            "last_name": "olivero"
        }
    ],
    "country": {
        "id": 222,
        "code": "VE",
        "name": "Venezuela"
    },
    "id_user": 7,
    "first_name": "luisana",
    "username": "luisagtx",
    "sex": "Mujer"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "El campo imagen de perfil no puede estar vacio"
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
    "detail": "no puedes subir mas de 6 imagenes en el profile"
  }
  ```
* Notes:
 
  **Max six images to upload to profile**
___

## Profile User Service
Get all profile image of user


**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/id//assign-image/

  **id** user id
* Method

  **GET**

* Url Params

  **None**

* Data Params
 
 **None**

* Success Response:
   * code: 200
    ```javascript
      [
          {
              "id": 3,
              "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png"
          },
          {
              "id": 4,
              "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg"
          }
      ]
    ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail":"error"
   }
   ``` 
* Notes:
 
  **None**
___
## Profile User Service
assign image in your profile

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/id/assign-image/id_image/

  **id** user id
  
  **id_image** id of image profile
* Method

  **PUT**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
   {
        "profile_images": [
        {
            "id": 3,
            "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png"
        },
        {
            "id": 4,
            "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg"
        }
    ],
    "description": "hola soy nuev en weedmatch me gusta la hierba brava :)",
    "direction": "Barrio 18 De Octubre, Maracaibo 4002, Zulia, Venezuela",
    "age": 23,
    "email": "luisanaolivero2@hotmail.com",
    "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
    "match_sex": "Mujer",
    "detail": "Tu imagen de perfil ha sido cambiada exitosamente",
    "credit_card": [
        {
            "number_card": "9864",
            "id": 2,
            "type_card": "visa",
            "first_name": "luisana",
            "year": "22",
            "month": "02",
            "last_name": "olivero"
        }
    ],
    "country": {
        "id": 222,
        "code": "VE",
        "name": "Venezuela"
    },
    "id_user": 7,
    "first_name": "luisana",
    "username": "luisagtx",
    "sex": "Mujer"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "no existe la imagen en tu profile"
   }
   ``` 
* Notes:
 
  **None**
___

## Profile User Service
Delete images of profile

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/id/delete-image/id_image/

  **id** user id

  **id_imagen** id of image profile
* Method

  **DELETE**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
   {
     "profile_images": [
        {
            "id": 3,
            "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png"
        }
    ],
    "description": "hola soy nuev en weedmatch me gusta la hierba brava :)",
    "direction": "Barrio 18 De Octubre, Maracaibo 4002, Zulia, Venezuela",
    "age": 23,
    "email": "luisanaolivero2@hotmail.com",
    "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
    "match_sex": "Mujer",
    "detail": "Se ha eliminado una imagen de tu perfil exitosamente",
    "images_upload": [
        {
            "id": 1,
            "image": "http://127.0.0.1:8000/media/profile_420/jira.png",
            "comment": "nueva en weedmatch lol jaja",
            "like": 0
        }
    ],
    "credit_card": [
        {
            "number_card": "9864",
            "id": 2,
            "type_card": "visa",
            "first_name": "luisana",
            "year": "22",
            "month": "02",
            "last_name": "olivero"
        }
    ],
    "country": {
        "id": 222,
        "code": "VE",
        "name": "Venezuela"
    },
    "id_user": 7,
    "first_name": "luisana",
    "username": "luisagtx",
    "sex": "Mujer"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "no existe la imagen en tu profile"
   }
   ``` 
* Notes:
 
  **None**
___

## Public Profile
see all information of user 420 feed

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080//public-profile/id/

**id** user id
* Method

  **GET**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
	   {
		"image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
	    "country": {
		"id": 222,
		"name": "Venezuela",
		"code": "VE"
	    },
	    "description": "hola soy nuev en weedmatch me gusta la hierba brava :)",
	    "username": "luisagtx",
	    "id_user": 7,
	    "distance": "4 km",
	    "age": 23,
	    "profile_images": [
		{
		    "image": "http://127.0.0.1:8000/media/profile/Captura-de-pantalla-2014-05-28-a-las-23.42.24_k00hq4Z.png",
		    "id": 3
		},
		{
		    "image": "http://127.0.0.1:8000/media/profile/10151841_1434099783497216_1940085989_n.jpg",
		    "id": 4
		}
	    ],
	    "first_name": "luisana"  
     }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "el usuario no se encuentra registrado en el sistema"
   }
   ``` 
* Notes:
 
  **None**
___

## Public Feed 420

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/public-feed/

* Method

  **GET**

* Url Params

  **None**

* Data Params
 
  **None**

* Success Response:
   * code: 200
    ```javascript
   {
      "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "image": "http://127.0.0.1:8000/media/profile_420/jira.png",
            "username": "luisagtx",
            "distance": "4 km",
            "time": "1 days",
            "first_name": "luisana",
            "id_user": 7,
            "id_image": 2
        }
    ]
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail":"error"
   }
   ``` 
* Notes:
 
  **The information shown will depend on the user's match configuration to show men, women or both**
___

## Upload Image 
upload image to public feed 420

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/public-image/

* Method

  **POST**

* Url Params

  **None**

* Data Params

  Form Data
  *image
  *comment

* Success Response:
   * code: 200
    ```javascript
   {
    "image": "http://127.0.0.1:8000/media/profile_420/Captura_de_pantalla_de_2017-08-30_10-26-08.png",
    "comment": "fumando mucho",
    "detail": "La imagen se ha subido a tu profile publico con exito",
    "id": 2,
    "like": 0
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "El campo imagen del feed publico no puede estar vacio"
   }
   ``` 
* Notes:
 
  **None**
___

## Upload Image

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/public-image/

* Method

  **GET**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
   {
   	"count": 1,
    	"next": null,
    	"previous": null,
    	"results":[
	    {
		"id": 1,
		"comment": "nueva en weedmatch lol jaja",
		"like": 0,
		"image": "http://127.0.0.1:8000/media/profile_420/jira.png"
	    },
	    {
		"id": 2,
		"comment": "fumando mucho",
		"like": 0,
		"image": "http://127.0.0.1:8000/media/profile_420/Captura_de_pantalla_de_2017-08-30_10-26-08.png"
	    }
    	]
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail":"error"
   }
   ``` 
* Notes:
 
  **None**
___

## Upload Image

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/public-image/id/like/id_user/
  
  **id** id image 
  
  **id_user** id the user to increment o decrement count to image
* Method

  **PUT**

* Url Params

  **None**

* Data Params
 ```javascript
 {
   "like":"true"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
     "detail": "se ha editado la imagen con exito,",
     "id": 1,
     "comment": "nueva en weedmatch lol jaja",
     "like": 1,
     "image": "http://127.0.0.1:8000/media/profile_420/jira.png"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "La imagen no existe en tu perfil publico"
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
    "detail": "el campo like no puede estar vacio"
  }
  ```
  
  or

  * code: 400
  ```javascript
  {
    "detail": "No se puede anexar un nuevo me gusta a su imagen publica"
  }
  ```
* Notes:
 
  **Is like send "true" increment like for this photo, in case to send "false" decrement like in 1**
___

## Upload Image

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/public-image/id/

 **id** id image
* Method

  **DELETE**

* Url Params

  **None**

* Data Params

  **None**

* Success Response:
   * code: 200
    ```javascript
   {
     "detail": "La imagen a sido borrada con exito de su perfil publico"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail":"La imagen no existe en tu feed publico o la has eliminado"
   }
   ``` 
* Notes:
 
  **None**
___

