# Payment services

## Credit Card Service
create a credit card for user account

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/payment/card/

* Method

  **POST**

* Url Params

  **None**

* Data Params
 ```javascript
 {
  "first_name":"luisana",
  "last_name": "olivero",
  "number_card":"4032123456789869",
  "type_card":"visa",
  "date_expiration":"2023-04-01"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
      "number_card": "9869",
      "detail": "La tarjeta de credito se ha agregado a tu cuenta con exito",
      "year": "23",
      "month": "04",
      "type_card": "visa",
      "first_name": "luisana",
      "id": 3,
      "last_name": "olivero"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
      "detail": {
        "number_card": "Ya esta registrado en tu cuenta ese numero de tarjeta"
    }
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
     "detail": {
        "type_card": [
            "unallowed value visas"
        ]
    }
  }
  ```
* Notes:
 
  **None**
___

## Credit card
get all credit card assign in user account

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/payment/card/
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
            "number_card": "9864",
            "year": "22",
            "month": "02",
            "type_card": "visa",
            "first_name": "luisana",
            "id": 2,
            "last_name": "olivero"
        },
        {
            "number_card": "9869",
            "year": "23",
            "month": "04",
            "type_card": "visa",
            "first_name": "luisana",
            "id": 3,
            "last_name": "olivero"
        }
    ]
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
     "detail": "error"
   }
   ``` 
* Notes:
 
  **if you call this service with the id of credit card only return one**
___
## Credit card
update the information of credit card

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/payment/card/id/

  **id** credit card id
* Method

  **PUT**

* Url Params

  **None**

* Data Params
 ```javascript
 {
   "first_name":"luisana",
   "last_name": "olivero",
   "number_card":"4032123456789869",
   "type_card":"visa",
   "date_expiration":"2024-09-01"
 } 
 ```

* Success Response:
   * code: 200
    ```javascript
   {
      "number_card": "9869",
      "detail": "La información de la tarjeta de credito se ha editado con exito",
      "year": "24",
      "month": "09",
      "type_card": "visa",
      "first_name": "luisana",
      "id": 3,
      "last_name": "olivero"
   }
   ```  
* Error Response:
  * code: 400
   ```javascript
   {
      "detail": {
        "number_card": "Ya esta registrado en tu cuenta ese numero de tarjeta"
    }
   }
   ``` 
  or

  * code: 400
  ```javascript
  {
    "detail": {
        "type_card": [
            "unallowed value visas"
        ]
    }
  }
  ```

  or
  * code: 404
   ```javascript
   {
     "detail": "No encontrado."
   }
   ```
* Notes:
 
  **None**
___
## Credit card
delete a credit card the user account

**TOKEN IS REQUIRED FOR THIS SERVICE**
* Url

  http://127.0.0.1:8080/payment/card/id/

  **id** credit card id
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
      "detail": "la tarjeta de credito ha sido eliminada de tu cuenta con exito"   
   }
   ```  
* Error Response:
  * code: 404
   ```javascript
   {
     "detail": "No encontrado."
   }
   ``` 
* Notes:
 
  **None**
___