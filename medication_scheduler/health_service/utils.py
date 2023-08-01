import datetime
import time
import smtplib
from email.mime.text import MIMEText
import pymongo
from medication_scheduler.settings import DOC_DB_URI, DOC_DB_NAME, EMAIL_SERVER, EMAIL_PORT, SENDER_EMAIL, \
    SENDER_PASSWORD, RECEIVER_EMAIL, SCHEDULES_COLLECTION,USERS_COLLECTION,PATIENTS_COLLECTION


class DbConnection:
    _instance = None
    _connection = None

    def __int__(self):
        self._connection = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def connect(self):
        if not self._connection:
            try:
                print(f"INFO | Connecting to DB: {DOC_DB_URI}")
                self._connection = pymongo.MongoClient(DOC_DB_URI)
            except Exception as e:
                print(f"ERROR | Unable to connect to DB due to error: {str(e)}")
                raise ConnectionError

    def get_collection(self, collection_name):
        return self._connection[DOC_DB_NAME][collection_name]


class Notification:
    def __init__(self):
        db_conn = DbConnection()
        db_conn.connect()
        self.email_server = EMAIL_SERVER
        self.email_port = EMAIL_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.receiver_email = RECEIVER_EMAIL
        self.medication_collection = db_conn.get_collection(SCHEDULES_COLLECTION)
        self.patient_collection=db_conn.get_collection(PATIENTS_COLLECTION)
        self.user_collection=db_conn.get_collection(USERS_COLLECTION)
    def send_email(self, subject, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email

            server = smtplib.SMTP(self.email_server, self.email_port)
            server.ehlo()
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, [self.receiver_email], msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email:", str(e))

    def get_medicines_by_time(self, current_time):
        result = self.medication_collection.find({"time": current_time})

        if result:

            return result
        else:
            return None
    def get_user_id_by_patient_id(self,patient_id):
        result=self.patient_collection.find(patient_id)
        if result:
            return result
        else:
            return None

    def check_and_remind(self):
        try:
            # Get the current time in 24-hour format
            current_time = datetime.datetime.now().strftime("%H")

            # Retrieve the medicines/actions corresponding to the current time
            medicines = self.get_medicines_by_time(current_time)



            # If medicines/actions are scheduled for the current time, send an email
            if medicines:
                subject = "Medication Reminder"
                message = f"Time to take medicines! The current time is: {current_time}\n"
                for item in medicines:
                    message += f"{item}\n"
                self.send_email(subject, message)

        except KeyboardInterrupt:
            print("Medication reminder program stopped.")


def my_scheduled_task():
    notification = Notification()
    while True:
        print("Executing scheduled task now...")
        notification.check_and_remind()
        # Setting time frame of mock scheduler as 1 hour.
        time.sleep(60*60)
        # This function will be executed at the scheduled time
