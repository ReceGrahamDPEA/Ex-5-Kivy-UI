import os
import time
import logging
import threading

os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from kivy.properties import ObjectProperty

import time as timetime
from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
IMAGE_SCREEN_NAME = 'image'
ANIMATED_SCREEN_NAME = 'animated'


class ProjectNameGUI(App):

    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

class DPEAButton(Button):
    """
    DPEAButton class
    """
    shadow_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "shadow.png")
    shadow_path = ObjectProperty(shadow_image_path)

    def __init__(self, **kwargs):
        """
        Specifies the background_color, background_normal, and size_hint for all instances
        :param kwargs: Arguments passed to the Button Instance
        """
        super(DPEAButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.size_hint = (None, None)
        self.original_colors = list()

    def on_press(self):
        """
        Overrides the Button default on_press to darken the color of the button.
        :return: None
        """
        super(DPEAButton, self).on_press()
        self.original_colors = self.color
        self.color = [i * 0.7 for i in self.original_colors]

    def on_touch_up(self, touch):
        """
        Overrides the Button default on_touch_up to revert the buttons color back to its original color.
        NOTE: This method is called for every widget onscreen
        :return: None
        """
        super(DPEAButton, self).on_touch_up(touch)

        # If button hasn't been pressed self.original colors is empty and will make the button color be black
        # So if the length is empty it hasn't been pressed so we return
        if len(self.original_colors) == 0:
            return

        self.color = self.original_colors



Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):

    Builder.load_file('AnimatedButtonScreen.kv')

    clicks = ObjectProperty()

    """
    Class to handle the main screen and its associated touch events
    """

    def counterButton(self):
        self.ids.count.clicks += 1
        self.ids.count.txt = str(self.ids.count.clicks)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def basicAnimation(self, widget):

        animation = Animation(pos=(100, 100), t = 'out_bounce', duration = 1) + Animation(size=(200,200), duration=5)
        animation.start(widget)

        SCREEN_MANAGER.current = 'animated'

        print("bless you")

class ImageScreen(Screen):

    Builder.load_file('ImageScreen.kv')

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

class AnimatedButtonScreen(Screen):

    def complexAnimation(self, widget):
        anim = Animation(pos=(80, 10))
        anim &= Animation(size=(800, 800), duration=2.)
        anim.start(widget)

        SCREEN_MANAGER.current = 'main'

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()



"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ImageScreen(name='image'))
SCREEN_MANAGER.add_widget(AnimatedButtonScreen(name='animated'))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
