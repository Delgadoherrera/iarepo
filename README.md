# UNUM_IA

## INSTALL:
    pip install -r requirements.txt

## DEPLOY FLASH:
    export FLASK_APP=__init__:app
    flask run

## DEPLOY GUNICORN:
    gunicorn -w 4 -b 127.0.0.1:5000 __init__:app

##  Preguntas de ejemplo:
    A nombre de quien esta la factura?
    A quien esta dirigido el documento?

### Pregunta JSON:

    La respuesta a devolver debe ser en formato json y que contenga: El código de pregunta, la pregunta y la respuesta. En caso de no encontrar una respuesta adecuada para una pregunta la respuesta debe ser un null. [P1,Pais donde se emitió la factura, texto], [P2,NIT (lo que comúnmente de denomina tax id) del emisor de la factura, numero sin separadores], [P3,Valor total de la factura, numero sin separadores y si tiene decimales usar el punto como decimal], [P4,Fecha de emisión de la facctura, fecha en formato aaaa/mm/dd]
