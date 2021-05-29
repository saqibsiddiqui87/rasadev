from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import csv

class ExportingInfo(Action):
    def name(self) -> Text:
        return "exporting_csv"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        with open("FromRasa.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("designation"), tracker.get_slot("location")])
                

class ValidateCogentForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number", "designation", "location"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"),
                                 Designation=tracker.get_slot("designation"))