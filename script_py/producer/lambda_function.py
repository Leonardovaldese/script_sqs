import boto3
import json

# Configurazione delle risorse
queue_url = "https://sqs.us-east-1.amazonaws.com/992382525644/MySQS"
region = "us-east-1"
auto_scaling_group_name = "AutoScalingSQS"

# Creazione di un client SQS
sqs_client = boto3.client("sqs", region_name=region)

# Creazione di un client Auto Scaling
auto_scaling_client = boto3.client("autoscaling", region_name=region)

# Funzione per inviare un messaggio JSON alla coda SQS
def send_message_to_sqs(message_body):
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body),
    )
    return response

# Funzione per generare e inviare il messaggio JSON del veicolo
def generate_and_send_vehicle_message():
    # Genera le informazioni sul veicolo
    message = {
        "vehicleId": "VH2001",
        "marca": "Honda",
        "modello": "Civic",
        "anno": 2020,
        "colore": "Blu",
        "chilometraggio": 15000
    }

    # Invia il messaggio alla coda SQS
    response = send_message_to_sqs(message)

    print(f"MessageId: {response['MessageId']}")
    print(f"Message body: {json.dumps(message, indent=2)}")

    # Avvia un'istanza dell'Auto Scaling Group
    response = auto_scaling_client.set_desired_capacity(
        AutoScalingGroupName=auto_scaling_group_name,
        DesiredCapacity=1
    )
    print("Auto Scaling instance started.")

# Funzione principale invocata da Lambda
def lambda_handler(event, context):
    generate_and_send_vehicle_message()
