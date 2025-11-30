import unittest
import os
import json
from smart_home.home import Home
from smart_home.room import Room
from smart_home.smart_bulb import SmartBulb
from smart_home.air_conditioner import AirConditioner
from smart_home.scheduler import Scheduler, InvalidTimeError
from smart_home.data_manager import DataManager

class TestSmartBulb(unittest.TestCase):
    def test_initial_state(self):
        bulb = SmartBulb("Test Bulb")
        self.assertFalse(bulb.status)
        self.assertEqual(bulb.intensity, 0)
        self.assertEqual(bulb.color, {'r': 255, 'g': 255, 'b': 255})

    def test_turn_on_off(self):
        bulb = SmartBulb("Test Bulb")
        bulb.turn_on()
        self.assertTrue(bulb.status)
        bulb.turn_off()
        self.assertFalse(bulb.status)

    def test_intensity(self):
        bulb = SmartBulb("Test Bulb")
        bulb.increase_intensity()
        self.assertEqual(bulb.intensity, 10)
        bulb.decrease_intensity()
        self.assertEqual(bulb.intensity, 0)
        bulb.increase_intensity(50)
        self.assertEqual(bulb.intensity, 50)
        bulb.increase_intensity(60)
        self.assertEqual(bulb.intensity, 100)
        bulb.decrease_intensity(110)
        self.assertEqual(bulb.intensity, 0)

    def test_color_change(self):
        bulb = SmartBulb("Test Bulb")
        bulb.change_color(100, 150, 200)
        self.assertEqual(bulb.color, {'r': 100, 'g': 150, 'b': 200})
        with self.assertRaises(ValueError):
            bulb.change_color(300, 100, 100)

class TestAirConditioner(unittest.TestCase):
    def test_initial_state(self):
        ac = AirConditioner("Test AC")
        self.assertFalse(ac.status)
        self.assertEqual(ac.temperature, 21)

    def test_turn_on_off(self):
        ac = AirConditioner("Test AC")
        ac.turn_on()
        self.assertTrue(ac.status)
        ac.turn_off()
        self.assertFalse(ac.status)
        self.assertEqual(ac.temperature, 16)

    def test_temperature(self):
        ac = AirConditioner("Test AC")
        ac.increase_intensity()
        self.assertEqual(ac.temperature, 22)
        ac.decrease_intensity()
        self.assertEqual(ac.temperature, 21)
        ac.increase_intensity(5)
        self.assertEqual(ac.temperature, 26)
        ac.increase_intensity(10)
        self.assertEqual(ac.temperature, 30)
        ac.decrease_intensity(20)
        self.assertEqual(ac.temperature, 16)

class TestRoom(unittest.TestCase):
    def test_add_device(self):
        room = Room("Living Room")
        bulb = SmartBulb("Lamp")
        room.add_device(bulb)
        self.assertIn(bulb, room.devices)
        with self.assertRaises(ValueError):
            room.add_device(bulb)

class TestHome(unittest.TestCase):
    def test_add_room_and_device(self):
        home = Home("My Home")
        home.add_room("Bedroom")
        room = home.get_room_by_name("Bedroom")
        self.assertIsNotNone(room)
        bulb = SmartBulb("Night Light")
        home.add_device_to_room(bulb, "Bedroom")
        self.assertIn(bulb, room.devices)
        with self.assertRaises(ValueError):
            home.add_room("Bedroom")
        with self.assertRaises(ValueError):
            home.add_device_to_room(bulb, "Kitchen")

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.bulb = SmartBulb("Programmable Bulb", is_programmable=True)
        self.scheduler = Scheduler(self.bulb)

    def test_add_event(self):
        self.scheduler.add_event("Monday", 10, 30, 0, "turn_on")
        self.assertEqual(len(self.scheduler.schedule), 1)
        event = self.scheduler.schedule[0]
        self.assertEqual(event['day'], "Monday")
        self.assertEqual(event['action'], "turn_on")

    def test_invalid_time(self):
        with self.assertRaises(InvalidTimeError):
            self.scheduler.add_event("Funday", 10, 30, 0, "turn_on")
        with self.assertRaises(InvalidTimeError):
            self.scheduler.add_event("Monday", 25, 30, 0, "turn_on")

    def test_delete_event(self):
        self.scheduler.add_event("Tuesday", 18, 0, 0, "turn_off")
        self.scheduler.delete_event(0)
        self.assertEqual(len(self.scheduler.schedule), 0)
        with self.assertRaises(IndexError):
            self.scheduler.delete_event(0)

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_home_data.json"
        self.home = Home("Test Home")
        self.home.add_room("Office")
        bulb = SmartBulb("Desk Lamp", is_programmable=True)
        self.home.add_device_to_room(bulb, "Office")
        scheduler = self.home.get_scheduler_for_device(bulb.id)
        scheduler.add_event("Friday", 9, 0, 0, "turn_on")


    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        DataManager.save_home_to_json(self.home, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        loaded_home = DataManager.load_home_from_json(self.test_file)
        self.assertIsNotNone(loaded_home)
        self.assertEqual(loaded_home.name, self.home.name)
        self.assertEqual(len(loaded_home.rooms), 1)
        
        loaded_room = loaded_home.get_room_by_name("Office")
        self.assertIsNotNone(loaded_room)
        self.assertEqual(len(loaded_room.devices), 1)
        
        loaded_bulb = loaded_room.devices[0]
        self.assertIsInstance(loaded_bulb, SmartBulb)
        
        loaded_scheduler = loaded_home.get_scheduler_for_device(loaded_bulb.id)
        self.assertIsNotNone(loaded_scheduler)
        self.assertEqual(len(loaded_scheduler.schedule), 1)
        self.assertEqual(loaded_scheduler.schedule[0]['day'], "Friday")


if __name__ == '__main__':
    unittest.main()
