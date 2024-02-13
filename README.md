# Documentazione Dettagliata

Questa documentazione illustra i passaggi necessari per creare e utilizzare una coda Amazon SQS standard, un gruppo di Auto Scaling EC2,bucket S3 e una funzione Lambda e la configurazione dei ruoli all’interno di IAM.  
Inoltre, descrive la funzione Lambda “producer” per l'invio di messaggi e uno script “consumer” scaricato da un bucket S3 per il processo di polling e stampa del messaggio mandato.

# Definizione dei Ruoli IAM e delle Relative Policy(IAM1.jpg,IAM2.jpg,IAM3.jpg,IAM4.jpg)
1. Accedi alla Console di Gestione AWS.
2. Nella barra di ricerca dei servizi, digita "IAM" e seleziona IAM dalla lista dei servizi disponibili.
3. Clicca su "Roles" nel menu di sinistra e successivamente su "Create role".
4. Scegli il servizio che avrà bisogno dell'accesso e clicca su "Next: Permissions".
5. Cerca e seleziona le policy appropriate per il servizio.
6. Prosegui con il processo di creazione del ruolo, assegnandogli un nome significativo e una descrizione, quindi clicca su "Create role".
7. Una volta creato il ruolo, assegna il ruolo agli utenti o alle risorse che necessitano l’accesso.
Questa procedura verrà ripetuta per ogni servizio che usufruiremo di conseguenza scrivo per ogni servizio il nome e le policy del ruolo creato:

servizio:EC2 Auto-Scaling;
nome ruolo: EC2ASforSQS;
Policy:
AutoScalingFullAccess;
AmazonSQSFullAccess;
AmazonS3FullAccess

servizio:LAMBDA
nome ruolo: LAforSQS;
Policy:
AutoScalingConsoleFullAccess;
AmazonSQSFullAccess;
CloudWatchFullAccess;
AWSLambda_FullAccess

# Creazione di una coda Amazon SQS (SQS1.jpg,SQS2.jpg,SQS3.jpg)
1. Accedi alla Console di Gestione AWS.
2. Nella barra di ricerca dei servizi, digita "SQS" e seleziona Amazon SQS dalla lista dei servizi disponibili.
3. Clicca sul pulsante "Create Queue" per iniziare il processo di creazione della coda SQS.
4. Specifica la configurazione della coda SQS:
- Nome della Coda: [MySQS]
- Tipo di Coda: Standard Queue
- Opzioni di Configurazione:
lascio tutte le impostazioni di default tranne ACCESS POLICY
send/receive:Only the specified AWS accounts, IAM users and roles
send:[inserisci l’arn  del ruolo dedicato alla lambda producer]
receive:[inserisci l’arn del ruolo dedicato all’autoscaling/ec2]

# Creazione del Launch Tamplates (LT1.jpg,LT2.jpg,LT3.jpg,LT4.jpg,LT5.jpg,LT6.jpg,LT7.jpg,LT8.jpg)
Prima di poter creare il gruppo di autoscaling bisogna creare Launch Tamplates nella quale si configura le EC2 che verranno create durante l’Autoscaling.
1. Accedi alla Console di Gestione AWS.
2. Nella barra di ricerca dei servizi, digita "EC2" e seleziona EC2 dalla lista dei servizi disponibili.
3. Nel menu di sinistra, clicca su "Launch Tamplates" e successivamente su "Create launch template".
4. Segui il processo per la creazione del launch template, fornendo  informazioni come il nome, la subnet, la configurazione dell'istanza EC2 e così via.
-Launch template name:TamplateSQS
Template version description:1(definisco la versione del Tamplate)
-Application and OS Images (Amazon Machine Image)
Quick Start
          - Amazon Machine Image (AMI): Amazon Linux 2023 AMI
          - Instance type: t2.micro

-Key pair name: Don't include in launch template
-Network settings
Subnet:Don't include in launch template
Select existing security group
   -Security groups:default VPC 
-Advanced details
IAM instance profile: EC2ASforSQS (ruolo creato nella sezione IAM)

User data:

- #!/bin/bash
- sudo su - ec2-user
- sudo yum install -y python3-pip  # Installa pip3
- sudo pip3 install boto3       # Installa la libreria boto3
- sudo pip3 install time        # Installa la libreria time
- #Scarica lo script da Amazon S3
- aws s3 cp s3://bucketsqs/script_sqs/consumer.py /home/ec2-user/consumer.py
- chmod +x /home/ec2-user/consumer.py
- python3 /home/ec2-user/consumer.py 


-Premi su “Create launch template”.

# Creazione Autoscaling Groups EC2 (AG1.jpg,AG2.jpg,AG3.jpg,AG4.jpg)
1.  Sulla dashboard di EC2 selezioniamo Auto Scaling Groups
2. Clicca su “Create Autoscaling group”
3. Definiamo i primi parametri:
  -Auto Scaling group name: “AutoScalingSQS”
  -Launch template: “TamplateSQS” (selezionabile)
4. Lascia i parametri di default tranne: 
  -Desired capacity:1
  -Min desired capacity:0
  -Max desired capacity:4
5. Clicca “NEXT” fino ad “REVIEW”, clicca Create Auto Scaling group.

# Creazione bucket S3 (BS3.jpg,BS3_1.jpg,BS3_2.jpg)
1.Nella console di gestione AWS, cerca e seleziona "Amazon S3" dal menu dei servizi.
2.Nella pagina di Amazon S3, fai clic sul pulsante "Crea bucket" per iniziare il processo di creazione di un nuovo bucket.
3.Configura le impostazioni del bucket:
   - Nome del bucket: “bucketsqs”
   - Regione AWS: “US East (N. Virginia) us-east-1”
4. lascio le impostazioni di default. ( per il nostro uso il bucket serve solamente per avere sempre a disposizione lo script consumer.py)
5. clicca su “create bucket”
6. crea una cartella all’interno del bucket col nome “script_sqs”
7. inserisci all’interno della cartella lo script  “consumer.py”


# Creazione di una Funzione Lambda (LMB1.jpg,LB2.jpg,LB3.jpg)
1. Nella barra di ricerca dei servizi, digita "Lambda" e seleziona Lambda dalla lista dei servizi disponibili.
2. Clicca sul pulsante "Create function" per iniziare il processo di creazione della funzione Lambda.
3. Seleziona l'opzione "Author from scratch" per creare una nuova funzione Lambda da zero.
4. Compila i seguenti campi nella finestra di configurazione della funzione Lambda:
  -Name: producer.py
  -Runtime: Python 3.12
  -Execution role:Use an existing role
  -Existing role: LAforSQS
5. Una volta configurati tutti i campi necessari, clicca su "Create function" per completare la creazione della funzione Lambda.
6. Aggiungi la destinazione dello script direttamente ad MySQS sia in condizione di On failure/On success
7. Inserisci all’interno di lambda_function.py il codice scritto per producer.py
8. Configuro il test event facendo “create new event” (esso viene usato per poter fare dei test del proprio script)


# RISULTATI DEI TEST(TEST.jpg,TEST1.jpg)
Dai risultati dei test emerge la corretta operatività del sistema. 
Lo script producer.py  inserito in Lambda genera il messaggio JSON e attiva una prima istanza dell'Auto Scaling, inviandolo successivamente a SQS. 
Al momento della creazione della prima istanza mediante i comandi forniti nell'User Data, 
il sistema è in grado di scaricare le librerie necessarie e avviare il programma consumer.py dal bucket S3 all'interno dell'istanza. 
Quest'ultimo monitora costantemente la coda di SQS, stampando i messaggi ricevuti e aggiornando dinamicamente il numero di istanze desiderate nell'Auto Scaling. 
Tale valore può variare da un minimo di 0 a un massimo di 4 istanze, garantendo così una gestione flessibile e ottimale delle risorse.

