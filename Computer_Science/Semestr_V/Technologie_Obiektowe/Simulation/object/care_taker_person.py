from .person import Person
from .memento_person import MementoPerson
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from state.i_state import IState
from state.healty_state import HealtyState
from state.immune_state import ImmunteState
from state.no_symptoms_state import NoSymptomsState
from state.symptoms_state import SymptomsState
from vector.vector_2D import Vector2D

class CareTakerPerson:
    def __init__(self) -> None:
        self.mementos = []
    
    def backup(self, list_person: list[Person]):
        self.mementos = []
        for person in list_person:
            self.mementos.append(person.save_to_memento())

    def save(self):
        root = ET.Element('root')
        root.tail = '\n'
        for memento in self.mementos:
            person = ET.SubElement(root, 'person')
            state_element = ET.SubElement(person, 'state')
            state_element.text = str(memento.get_state())
            position_element = ET.SubElement(person, 'position_x')
            position_element.text = str(memento.get_position().get_x())
            position_element = ET.SubElement(person, 'position_y')
            position_element.text = str(memento.get_position().get_y())
            velocity_element = ET.SubElement(person, 'velocity_x')
            velocity_element.text = str(memento.get_velocity().get_x())
            velocity_element = ET.SubElement(person, 'velocity_y')
            velocity_element.text = str(memento.get_velocity().get_y())
            on_screen_element = ET.SubElement(person, 'on_screen')
            on_screen_element.text = str(memento.get_on_screen())
            time_near_unhealthy_element = ET.SubElement(person, 'time_near_unhealthy')
            time_near_unhealthy_element.text = str(memento.get_time_near_unhealthy())
            time_near_no_symptoms_element = ET.SubElement(person, 'time_near_no_symptoms')
            time_near_no_symptoms_element.text = str(memento.get_time_near_no_symptoms())
            time_to_recover_element = ET.SubElement(person, 'time_to_recover')
            time_to_recover_element.text = str(memento.get_time_to_recover())
            max_width_element = ET.SubElement(person, 'max_width')
            max_width_element.text = str(memento.get_max_width())
            max_height_element = ET.SubElement(person, 'max_height')
            max_height_element.text = str(memento.get_max_height())
            person.tail = '\n'
        tree = ET.ElementTree(root)
        tree.write('backup_population.xml', encoding='utf-8', xml_declaration=True)

    def restore(self):
        tree = ET.parse('backup_population.xml')
        root = tree.getroot()
        self.mementos = []
        for person in root.findall('person'):
            state = person.find('state').text
            position_x = float(person.find('position_x').text)
            position_y = float(person.find('position_y').text)
            velocity_x = float(person.find('velocity_x').text)
            velocity_y = float(person.find('velocity_y').text)
            on_screen = bool(person.find('on_screen').text)
            time_near_unhealthy = int(person.find('time_near_unhealthy').text)
            time_near_no_symptoms = int(person.find('time_near_no_symptoms').text)
            time_to_recover = int(person.find('time_to_recover').text)
            max_width = float(person.find('max_width').text)
            max_height = float(person.find('max_height').text)

            state_instance: IState
            if state == "green":
                state_instance = HealtyState()
            elif state == "blue":
                state_instance = ImmunteState()
            elif state == "red":
                state_instance = SymptomsState()
            elif state == "yellow":
                state_instance = NoSymptomsState()

            position = Vector2D(position_x, position_y)
            velocity = Vector2D(velocity_x, velocity_y)
            
            memento = MementoPerson(state_instance, position, velocity, on_screen, time_near_unhealthy, time_near_no_symptoms, time_to_recover, max_width, max_height)

            self.mementos.append(memento)

    def get_mementos(self):
        return self.mementos

        



    