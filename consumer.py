import boto3
import json
import time

# Configurazione delle risorse
queue_url = "https://sqs.us-east-1.amazonaws.com/992382525644/MySQS"
region = "us-east-1"
max_instances = 4

# Creazione dei clienti per SQS e Autoscaling
sqs_client = boto3.client("sqs", region_name=region)
autoscaling_client = boto3.client("autoscaling", region_name=region)

def update_autoscaling(num_messages):
    # Calcola il numero di istanze da scalare
    num_instances = min(max_instances, num_messages)
    
    # Ottieni il nome del gruppo di autoscaling
    asg_name = "AutoScalingSQS"
    
    # Aggiorna il numero di istanze del gruppo di autoscaling
    autoscaling_client.set_desired_capacity(
        AutoScalingGroupName=asg_name,
        DesiredCapacity=num_instances,
        HonorCooldown=False
    )

def main():
    try:
        while True:
            # Ottieni il numero di messaggi nella coda SQS
            queue_attributes = sqs_client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            num_messages = int(queue_attributes['Attributes']['ApproximateNumberOfMessages'])
            
            # Stampa il numero di messaggi nella coda SQS
            print("Numero di messaggi nella coda SQS:", num_messages)
            
            # Aggiorna l'autoscaling in base al numero di messaggi nella coda
            update_autoscaling(num_messages)
            
            # Polling dei messaggi dalla coda SQS
            response = sqs_client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            
            # Estrai i messaggi ricevuti
            messages = response.get('Messages', [])
            for message in messages:
                # Stampa il messaggio ricevuto sull'output standard
                print("Messaggio ricevuto:", message['Body'])

                # Elimina il messaggio dalla coda SQS dopo l'elaborazione
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )

            # Stampa tutti i messaggi ricevuti come file JSON
            if messages:
                with open("messages.json", "w") as json_file:
                    json.dump(messages, json_file, indent=4)
                    print("Messaggi salvati come file JSON.")

            # Attendi 60 secondi prima di eseguire nuovamente il polling dei messaggi
            time.sleep(60)

    except Exception as e:
        print("Errore durante il polling dei messaggi SQS:", str(e))

if __name__ == "__main__":
    main()

