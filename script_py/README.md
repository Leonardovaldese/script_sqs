PRODUCER.PY


Questo codice Python si occupa di monitorare una coda Amazon Simple Queue Service (SQS) e di gestire l'autoscaling in base al numero di messaggi presenti nella coda. 
Il codice importa le librerie necessarie, tra cui `boto3` per interagire con i servizi AWS, `json` per la manipolazione dei dati JSON e `time` per la gestione del tempo.
Viene configurata la coda SQS di interesse, specificando l'URL della coda (`queue_url`) e la regione AWS (`region`). 
Si specifica il numero massimo di istanze per l'autoscaling (`max_instances`) per poter fare avviare il meccanismo del consumer.py.
Crea i client per SQS e Autoscaling utilizzando `boto3`.
Viene definita la funzione `update_autoscaling(num_messages)` che calcola il numero di istanze da scalare in base al numero di messaggi nella coda SQS e aggiorna il numero di istanze nel gruppo di autoscaling.
La funzione principale `main()` viene definita per eseguire il polling della coda SQS, ricevere e elaborare i messaggi.
Nel ciclo principale `while True`,vengono ricevuti i messaggi dalla coda SQS utilizzando `receive_message()` ed elaborati uno per uno, 
il codice ottiene il numero approssimativo di messaggi nella coda SQS e lo stampa a schermo e successivamente eliminati dalla coda utilizzando `delete_message()'.
L'autoscaling viene aggiornato in base al numero di messaggi presenti nella coda.
Il programma attende 60 secondi prima di eseguire nuovamente il polling della coda SQS.
In caso di errori durante l'esecuzione, viene stampato un messaggio di errore.
Il codice è progettato per essere eseguito in modo continuo, 
monitorando costantemente la coda SQS e regolando dinamicamente il numero di istanze in base al carico di lavoro.
