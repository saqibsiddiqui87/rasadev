from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import csv
import re
from rasa_sdk.forms import FormAction
from twilio.rest import Client
import random
from rasa_sdk.types import DomainDict
import requests
import time




class ExportingInfoInterview(Action):
    def name(self) -> Text:
        return "exporting_csv_interview"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        with open("FromRasaInterview.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("designation"), tracker.get_slot("location")])

class ExportingInfoPF(Action):
    def name(self) -> Text:
        return "exporting_csv_pf"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        with open("FromRasaPF.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("employee_id")])

class ExportingInfoESIC(Action):
    def name(self) -> Text:
        return "exporting_csv_esic"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        with open("FromRasaESIC.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("employee_id")])

class ExportingInfoSales(Action):
    def name(self) -> Text:
        return "exporting_csv_sales"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        with open("FromRasaSales.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("company"),  tracker.get_slot("time")])

                
class ActionRestart(Action):

  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      # custom behavior

      return [...]


class SendingOTP(Action):
    def name(self) -> Text:
        return "sendingOTP"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]: 
        global number
        randomnumber = random.randint(1000,9999)
        number = randomnumber
        response = requests.post("http://site.ping4sms.com/sendsms/?token=7d6a8fd620b4b19bad7adedd6b69dc6d&credit=2&sender=COGENT&message=Your%20OTP%20is%20"+ str(number) + ".%20Please%20do%20not%20share%20it%20with%20anyone.%20Thanks,%20Cogent%20E%20Services%20Pvt%20Ltd.&number=" + str(tracker.get_slot("number")) + "&templateid=1207162270187985439")

class SendingEmailInterview(Action):
    def name(self) -> Text:
        return "sendingEmailInteriew"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.post("http://lb.cogentlab.com/BotMailer/Service.asmx/mail?mailto=mailtest@cogenteservices.com&mailcc=&mailbcc=&subject=Interview Info mail&body=" + str(tracker.get_slot("name")) +  " " + str(tracker.get_slot("number")) +  " " + str(tracker.get_slot("designation")) +  " " + str(tracker.get_slot("location")) + "&key=jkknnbh5646500loon09i")
        


class SendingEmailPF(Action):
    def name(self) -> Text:
        return "sendingEmailPF"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.get("http://lb.cogentlab.com/BotMailer/Service.asmx/mail?mailto=mailtest@cogenteservices.com&mailcc=&mailbcc=&subject=PF mail&body=" + str(tracker.get_slot("name")) +  " " + str(tracker.get_slot("number")) +  " " + str(tracker.get_slot("employee_id")) + "&key=jkknnbh5646500loon09i")

class SendingEmailESIC(Action):
    def name(self) -> Text:
        return "sendingEmailESIC"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.get("http://lb.cogentlab.com/BotMailer/Service.asmx/mail?mailto=mailtest@cogenteservices.com&mailcc=&mailbcc=&subject=ESIC%20mail&body=" + str(tracker.get_slot("name")) +  "%20" + str(tracker.get_slot("number")) +  "%20" + str(tracker.get_slot("employee_id")) + "&key=jkknnbh5646500loon09i")

class SendingEmailSales(Action):
    def name(self) -> Text:
        return "sendingEmailSales"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.get("http://lb.cogentlab.com/BotMailer/Service.asmx/mail?mailto=mailtest@cogenteservices.com&mailcc=&mailbcc=&subject=Sales Info mail&body=" + str(tracker.get_slot("name")) +  " " + str(tracker.get_slot("number")) +  " " + str(tracker.get_slot("company")) +  " " + str(tracker.get_slot("day")) +  " " + str(tracker.get_slot("time")) + "&key=jkknnbh5646500loon09i")

class ValidateCogentFormOTP(FormValidationAction, SendingOTP):
    def name(self) -> Text:
        return "validate_cogent_form_otp"
    
    def validate_otp(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        global number
        print(str(number) +":number")
        print(str(tracker.latest_message.get('text')) + ":otp")
        if str(number) == str(tracker.get_slot("otp")): #and len(slot_value) == 4: #tracker.latest_message.text
            dispatcher.utter_message(text=f"OTP verified please proceed")
            return {"otp": slot_value}

        else:
            dispatcher.utter_message(text=f"Inavlid OTP, please re enter")
            return {"otp": None}



class ValidateCogentFormNumber(FormValidationAction):
    def name(self) -> Text:
        return "validate_cogent_form_init"
    
    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        if len(slot_value) == 10:
            return {"number": slot_value}
        else:
            dispatcher.utter_message(text=f"Please enter a valid 10 digit mobile number")
            return {"number": None}

class ValidateCogentFormNumber(FormValidationAction):
    def name(self) -> Text:
        return "validate_cogent_form_pf"
    
    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        global number
        randomnumber = random.randint(1000,9999)
        number = randomnumber
        response = requests.post("http://site.ping4sms.com/sendsms/?token=7d6a8fd620b4b19bad7adedd6b69dc6d&credit=2&sender=COGENT&message=Your%20OTP%20is%20"+ str(number) + ".%20Please%20do%20not%20share%20it%20with%20anyone.%20Thanks,%20Cogent%20E%20Services%20Pvt%20Ltd.&number=" + str(tracker.get_slot("number")) + "&templateid=1207162270187985439")
        if len(slot_value) == 10:
            return {"number": slot_value}
        else:
            dispatcher.utter_message(text=f"Please enter a valid 10 digit mobile number")
            return {"number": None}

    def validate_otp(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        global number
        print(str(number) +":number")
        print(str(tracker.latest_message.get('text')) + ":otp")
        if str(number) == str(tracker.get_slot("otp")): #and len(slot_value) == 4: #tracker.latest_message.text
            dispatcher.utter_message(text=f"OTP verified please proceed")
            return {"otp": slot_value}

        else:
            dispatcher.utter_message(text=f"Inavlid OTP, please re enter")
            return {"otp": None}

class ValidateCogentFormNumber(FormValidationAction):
    def name(self) -> Text:
        return "validate_cogent_form_esic"
    
    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        global number
        randomnumber = random.randint(1000,9999)
        number = randomnumber
        response = requests.post("http://site.ping4sms.com/sendsms/?token=7d6a8fd620b4b19bad7adedd6b69dc6d&credit=2&sender=COGENT&message=Your%20OTP%20is%20"+ str(number) + ".%20Please%20do%20not%20share%20it%20with%20anyone.%20Thanks,%20Cogent%20E%20Services%20Pvt%20Ltd.&number=" + str(tracker.get_slot("number")) + "&templateid=1207162270187985439")

        if len(slot_value) == 10:
            return {"number": slot_value}
        else:
            dispatcher.utter_message(text=f"Please enter a valid 10 digit mobile number")
            return {"number": None}

    def validate_otp(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text,Any]:
        global number
        print(str(number) +":number")
        print(str(tracker.latest_message.get('text')) + ":otp")
        if str(number) == str(tracker.get_slot("otp")): #and len(slot_value) == 4: #tracker.latest_message.text
            dispatcher.utter_message(text=f"OTP verified please proceed")
            return {"otp": slot_value}

        else:
            dispatcher.utter_message(text=f"Inavlid OTP, please re enter")
            return {"otp": None}


class PFverifying(Action):
    def name(self) -> Text:
        return "verify_pf"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.get("https://ems.cogentlab.com/erpm/Services/empinfo_pf_esic.php?key=pfesic&empid=" + str(tracker.get_slot("employee_id")))
        data1 = response.json()
        print(str(response))
        status = data1['Status']
        print(type(status))
        print(str(status))
        if status == "1":
            data2 = data1['data'][0]
            data3 = data2['mobile']
            print(data3)
            print(data2)     
            pfno = data2['uan_no']
            print(pfno)
            if str(tracker.get_slot('number')) == str(data3):
                dispatcher.utter_message(text=f"Thanks for verifying details, your PF number is " + str(pfno))
            else:
                dispatcher.utter_message(text=f"The phone number corresponding to this employee ID doesn't match with the one you provided, please check your info and try again, if problem persists please contact email@email.com")
                return {"number": None, "otp": None}
        else:
            dispatcher.utter_message(text=f"Your employee ID seems incorrect, if you are a former employee, please contact email@email.com")
            return {"employee_id": None}
           

class ESICVerifying(Action):
    def name(self) -> Text:
        return "verify_esic"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        response = requests.get("https://ems.cogentlab.com/erpm/Services/empinfo_pf_esic.php?key=pfesic&empid=" + str(tracker.get_slot("employee_id")))
        print(str(response))
        data1 = response.json()
        status = data1['Status']
        print(status)
        if status == "1":
            data2 = data1['data'][0]
            print(data2)
            data3 = data2['mobile']
            print(data3)
            esicno = data2['esi_no']
            print(esicno)
            if str(tracker.get_slot('number')) == str(data3):
                dispatcher.utter_message(text="Thanks for verifying details, your ESIC number is " + str(esicno))
            else:
                dispatcher.utter_message(text="The phone number corresponding to this employee ID doesn't match with the one you provided, please check your info and try again, if problem persists please contact email@email.com")
                return {"number": None, "otp": None}
              
        else:
            dispatcher.utter_message(text="Your employee ID seems incorrect, if you are a former employee, please contact email@email.com")
            return {"employee_id": None}
  