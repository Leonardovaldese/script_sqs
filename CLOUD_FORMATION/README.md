# README
![template1-designer.png](.CLOUD_FORMATION/template1-designer.png)
# Descrizione del File YAML
Il file YAML contiene la definizione delle risorse AWS da creare utilizzando CloudFormation. Di seguito sono elencate le risorse principali e i loro ruoli all'interno dell'infrastruttura:

**Parametri**: Definisce i parametri configurabili utilizzati durante la creazione dello stack CloudFormation.
**Risorse**: Elenco delle risorse AWS create durante il deployment dello stack CloudFormation, tra cui:
- _Ruoli IAM_
- _VPC e relative subnet_
- _Gruppi di sicurezza_
- _Code SQS_
- _Funzioni Lambda_
- _Gruppi di Auto Scaling_
- _Allarmi di CloudWatch_

## Risorsa da creare
- AWS S3 per l'archiviazione dei file

## Preparazione
Prima di eseguire lo script, è necessario preparare l'ambiente seguendo questi passaggi:

1. Creare un bucket S3 su AWS.
2. All'interno del bucket S3, creare una cartella chiamata `script_sqs`.
3. Caricare i file necessari per lo script ( `consumer.py` e `producer-233332.zip`) nella cartella `script_sqs`.

## Esecuzione dello Script
Prima di creare tutte le risorse, verrà richiesto di modificare alcune configurazioni:

1. **Nome del Bucket S3:** Prima di eseguire lo stack CloudFormation, assicurati di avere un bucket S3 dove verranno caricati gli script necessari. Inserisci il nome del bucket nella sezione S3BucketName dello stack.

2. **URL dell'Oggetto all'interno del Bucket:** Assicurati di avere il percorso corretto del "consumer.py" all'interno del bucket S3. Questo URL sarà utilizzato per scaricare lo script `consumer.py` sull'istanza EC2. Modifica l'URL nell'User Data dello stack CloudFormation.

Esempio di User Data:

UserData:
<pre>
  Fn::Base64: |
    #!/bin/bash 
    sudo su - ec2-user 
    sudo yum install -y python3-pip 
    sudo pip3 install boto3 /
    aws s3 cp s3://nome_del_bucket/script_sqs/consumer.py /home/ec2-user/consumer.py  
    chmod +x /home/ec2-user/consumer.py 
    python3 /home/ec2-user/consumer.py 
</pre>
