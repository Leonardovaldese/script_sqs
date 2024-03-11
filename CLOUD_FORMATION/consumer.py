import boto3
import json
import time

region = "us-east-1"  # Regione AWS

def get_queue_url(queue_name, region):
    sqs_client = boto3.client('sqs', region_name=region)
    response = sqs_client.list_queues(QueueNamePrefix=queue_name)
    queue_urls = response.get('QueueUrls', [])
    if not queue_urls:
        raise ValueError(f"Queue with name '{queue_name}' not found in region '{region}'")
    return queue_urls[0]

def main():
    queue_name = "MySQS1"  # Nome della coda SQS da cercare
    try:
        queue_url = get_queue_url(queue_name, region)
        print("URL della coda SQS:", queue_url)
        main1(queue_url)  # Passa l'URL della coda SQS come parametro a main1()
    except ValueError as e:
        print(e)

# Creazione del cliente per SQS
sqs_client = boto3.client("sqs", region_name=region)

def main1(queue_url):
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

            # Polling dei messaggi dalla coda SQS solo se ci sono messaggi presenti
            if num_messages > 0:
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

