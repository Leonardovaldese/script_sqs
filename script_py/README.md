# PRODUCER.PY


Questo codice Python interagisce con i servizi AWS SQS (Amazon Simple Queue Service) e Autoscaling utilizzando la libreria Boto3.
-Importa le librerie boto3 e json, necessarie per interagire con i servizi AWS e per la manipolazione dei dati JSON.

-Configura le risorse AWS specificando l'URL della coda SQS (queue_url), la regione (region) e il nome del gruppo di Autoscaling (auto_scaling_group_name).

-Crea un client per SQS e un client per Autoscaling utilizzando boto3.client().

-Definisce una funzione send_message_to_sqs(message_body) che invia un messaggio JSON alla coda SQS specificata. La funzione prende come argomento il corpo del messaggio da inviare, lo serializza in formato JSON utilizzando json.dumps() e lo invia alla coda SQS utilizzando sqs_client.send_message().

-Definisce una funzione generate_and_send_vehicle_message() che genera un messaggio JSON contenente informazioni su un veicolo (come ID, marca, modello, anno, colore e chilometraggio) utilizzando un dizionario Python. 
 Questo messaggio viene quindi inviato alla coda SQS utilizzando la funzione send_message_to_sqs() appena definita. Dopo l'invio del messaggio, viene stampato l'ID del messaggio e il corpo del messaggio.
 
-Dopo l'invio del messaggio alla coda SQS, la funzione avvia un'istanza del gruppo di Autoscaling utilizzando auto_scaling_client.set_desired_capacity(), impostando il numero desiderato di istanze a 1.

-Definisce una funzione principale lambda_handler(event, context) che viene invocata quando la funzione Lambda è attivata. In questo caso, la funzione generate_and_send_vehicle_message() viene chiamata per generare e inviare il messaggio JSON del veicolo alla coda SQS.








# CONSUMER.PY


Questo codice Python si occupa di monitorare una coda Amazon Simple Queue Service (SQS) e di gestire l'autoscaling in base al numero di messaggi presenti nella coda. 

-Il codice importa le librerie necessarie, tra cui `boto3` per interagire con i servizi AWS, `json` per la manipolazione dei dati JSON e `time` per la gestione del tempo.

-Viene configurata la coda SQS di interesse, specificando l'URL della coda (`queue_url`) e la regione AWS (`region`). 

-Specifica il numero massimo di istanze per l'autoscaling (`max_instances`).

-Crea i client per SQS e Autoscaling utilizzando `boto3`.

-Viene definita la funzione `update_autoscaling(num_messages)` che calcola il numero di istanze da scalare in base al numero di messaggi nella coda SQS e aggiorna il numero di istanze nel gruppo di autoscaling.

-La funzione principale `main()` viene definita per eseguire il polling della coda SQS, ricevere e elaborare i messaggi.

-Nel ciclo principale `while True`,vengono ricevuti i messaggi dalla coda SQS utilizzando `receive_message()` ed elaborati uno per uno, 
 il codice ottiene il numero approssimativo di messaggi nella coda SQS e lo stampa a schermo e successivamente eliminati dalla coda utilizzando `delete_message()'.
 
-L'autoscaling viene aggiornato in base al numero di messaggi presenti nella coda.

-Il programma attende 60 secondi prima di eseguire nuovamente il polling della coda SQS.

-In caso di errori durante l'esecuzione, viene stampato un messaggio di errore.

-Il codice è progettato per essere eseguito in modo continuo, 
 monitorando costantemente la coda SQS e regolando dinamicamente il numero di istanze in base al carico di lavoro.
