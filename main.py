import webbrowser
import geocoder
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import OneLineAvatarIconListItem, ImageLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import NumericProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from connectivity import l,insert_user,check_login,email_registered,signup_check
from connectivity import is_valid_email,otp,send_otp_via_email,generate_otp,show_welcome_email
from sign import show_wrong_password, show_wrong_password_email,show_wrong_otp
from sign import close_dialog, reload_signup_screen, reload_login_screen, show_missing_dialog, show_already_registered_dialog
from sign import reload_current_screen, handle_successful_signup,show_error_email_format,reload_main_screen


# ✅ Set Window Size for Mobile View
Window.size = (360, 640)
Window.clearcolor = (0.96, 0.98, 1, 1)
# --------------------- Screens ---------------------
from kivy.lang import Builder


class SplashScreen(MDScreen):
    def on_enter(self):
        self.start_progress()

    def start_progress(self):
        Clock.schedule_interval(self.update_progress, 0.05)

    def update_progress(self, dt):
        progress_bar = self.ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 5
        else:
            Clock.unschedule(self.update_progress)
            self.manager.current = "carpool"

class LoginScreen(MDScreen):
    def login_user(self):
        self.manager.current = "destination"

class RegisterScreen(MDScreen):
    def register_user(self):
        print("User Registered Successfully!")
        self.manager.current = "login"

class OTPScreen(MDScreen):
    def move_focus(self, instance):
        if instance.text:
            if instance == self.ids.field1:
                self.ids.field2.focus = True
            elif instance == self.ids.field2:
                self.ids.field3.focus = True
            elif instance == self.ids.field3:
                self.ids.field4.focus = True
            elif instance == self.ids.field4:
                self.verify_otp()

    def verify_otp(self):
        otp = (
            self.ids.field1.text +
            self.ids.field2.text +
            self.ids.field3.text +
            self.ids.field4.text
        )
        print(f"Entered OTP: {otp}")
        if otp == "1234":
            print("✅ OTP Verified!")
        else:
            print("❌ Incorrect OTP")

class DestinationScreen(MDScreen):
    def show_route(self):
        destination = self.ids.destination_input.text.replace(" ", "+")
        if destination:
            g = geocoder.ip("me")
            if g.latlng:
                lat, lon = g.latlng
                maps_url = f"https://www.google.com/maps/dir/{lat},{lon}/{destination}/"
                webbrowser.open(maps_url)
                Clock.schedule_once(lambda dt: self.goto_drivers(), 3)
            else:
                print("Could not determine location. Ensure GPS is on.")
        else:
            print("Enter a valid destination")

    def goto_drivers(self):
        self.manager.current = "home"
class PassengerDetailsScreen(MDScreen):
    def on_enter(self):
        # Fade in the passenger details card
        details_card = self.ids.details_card
        anim = Animation(opacity=1, duration=0.5, transition="in_out_quad")
        anim.start(details_card)

        # Slide in the reviews from the bottom
        for i, review in enumerate(self.ids.reviews_container.children):
            anim = Animation(pos_hint={"center_y": 0.5 + i * 0.3}, duration=0.5 + i * 0.1, transition="out_quad")
            anim.start(review)

class HomeScreen(MDScreen):
    def show_route(self):
        destination = self.ids.destination_input.text.replace(" ", "+")
        if destination:
            g = geocoder.ip("me")
            if g.latlng:
                lat, lon = g.latlng
                maps_url = f"https://www.google.com/maps/dir/{lat},{lon}/{destination}/"
                webbrowser.open(maps_url)
                Clock.schedule_once(lambda dt: self.goto_drivers(), 3)
            else:
                print("Could not determine location. Ensure GPS is on.")
        else:
            print("Enter a valid destination")

class CarpoolScreen(MDScreen):
    pass

class RideDetailsScreen(MDScreen):
    pass

class OfferRideScreen(MDScreen):
    def go_home(self):
        self.manager.current = "home"

class RequestRideScreen(MDScreen):
    pass

class DriverSelectionScreen(MDScreen):  
    pass

class ScheduleRideScreen(MDScreen):
    pass
class RideBookingScreen(MDScreen):
    pass

class RideSelectionScreen(MDScreen):
    pass

class ProfileScreen(MDScreen):
    pass

class RideSummaryScreen(MDScreen):
    pass

class ChangeRideScreen(MDScreen):
    pass

class ChatBotScreen(MDScreen):
    pass

class ServicesScreen(MDScreen):
    pass

class NotificationScreen(MDScreen):
    pass

class AvailableRidesScreen(MDScreen):
    pass
# --------------------- Utility Classes ---------------------

class Tab(MDTabsBase, FloatLayout):
    icon = ""
    title = ""

class RideOptionsDialog(BoxLayout):
    pass
class RegisterScreen(MDScreen):
    def on_pre_enter(self):
        self.ids.new_username.text = ""
        self.ids.new_licence.text = ""
        self.ids.new_email.text = ""
        self.ids.new_password.text = ""
# # class LoginScreen(MDScreen):
#     def on_pre_enter(self):
#         self.ids.email.text = ""
#         self.ids.password.text = ""


# --------------------- App Class ---------------------

class CarpoolApp(MDApp):
    current_tagline = StringProperty("Your Journey Begins Here")
    progress_value = NumericProperty(0)
    
    taglines = [
        "Carpooling: A breath of fresh air",
        "Share the ride, save the planet",
        "Connecting Destinations, Connecting Lives",
        "Go Green, Go Together"
    ]
    current_index = 0

    def open_url(self, url):
        webbrowser.open(url)

    def build(self):
        

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_palette = "Gray"  # Use a neutral color
        
        
        
        # ✅ Load KV file
        #Builder.load_file("main.kv")
        # Load all KV files
        Builder.load_file('splash.kv')
        Builder.load_file('carpool.kv')
        Builder.load_file('login.kv')
        Builder.load_file('register.kv')
        Builder.load_file('otp.kv')
        Builder.load_file('scheduleride.kv')
        Builder.load_file('destination.kv')
        Builder.load_file('home.kv')
        Builder.load_file('offeride.kv')
        Builder.load_file('passengerdetails.kv')
        Builder.load_file('requestride.kv')
        Builder.load_file('ridedetails.kv')
        Builder.load_file('ridebooking.kv')
        Builder.load_file('rideselection.kv')
        Builder.load_file('profile.kv')
        Builder.load_file('ridesummary.kv')
        Builder.load_file('changeride.kv')
        Builder.load_file('chatbot.kv')
        Builder.load_file('services.kv')
        Builder.load_file('notifications.kv')
        Builder.load_file('availablerides.kv')
        # ✅ Screen Manager
        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(OTPScreen(name="otp"))
        sm.add_widget(DestinationScreen(name="destination"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CarpoolScreen(name="carpool"))
        sm.add_widget(ScheduleRideScreen(name="schedule"))
        sm.add_widget(OfferRideScreen(name="offer_ride"))
        sm.add_widget(RequestRideScreen(name="request_ride"))
        sm.add_widget(RideDetailsScreen(name="ride_details"))
        sm.add_widget(DriverSelectionScreen(name="driver_selection"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(OTPScreen(name="otp"))
        sm.add_widget(ScheduleRideScreen(name="schedule"))
        sm.add_widget(PassengerDetailsScreen(name="passenger_details"))
        sm.add_widget(RideBookingScreen(name="ridebooking"))
        sm.add_widget(RideSelectionScreen(name="ride_selection"))
        sm.add_widget(ProfileScreen(name= "profile"))
        sm.add_widget(RideSummaryScreen(name='ride_summary'))
        sm.add_widget(ChangeRideScreen(name='change_ride'))
        sm.add_widget(ChatBotScreen(name="chatbot"))
        sm.add_widget(ServicesScreen(name="services"))
        sm.add_widget(NotificationScreen(name="notifications"))
        sm.add_widget(AvailableRidesScreen(name='available_rides'))
        return sm
        return OTPScreen()
    def check(self,new_username,new_licence,new_email,new_password):
        if not new_username.text or not new_licence.text or not  new_email.text or not new_password.text:
             self.saved_new_email = new_email.text
             self.saved_new_password = new_password.text
             self.show_missing_dialog("All fields are required")
             
        else:
            signup_check(self,new_username.text,new_licence.text, new_email.text, new_password.text)
    # Function to check where login details of user are correct are not
    def login(self,email,password):
        if not email.text or not password.text:
            # Show error dialog
            self.show_missing_dialog("Both email and password are required for login.")
        else:
            check_login(self,email.text,password.text)
    is_valid_email=is_valid_email
    show_error_email_format=show_error_email_format
    close_dialog = close_dialog
    l=l
    show_welcome_email=show_welcome_email
    show_missing_dialog=show_missing_dialog
    show_wrong_otp=show_wrong_otp
    reload_main_screen=reload_main_screen
    otp=otp
    generate_otp=generate_otp
    send_otp_via_email_=send_otp_via_email
    reload_signup_screen = reload_signup_screen
    reload_login_screen = reload_login_screen
    show_wrong_password=show_wrong_password
    show_wrong_password_email=show_wrong_password_email
    show_already_registered_dialog = show_already_registered_dialog
    reload_current_screen = reload_current_screen
    handle_successful_signup = handle_successful_signup


    def on_start(self):
        # Start progress bar animation
        self.animate_progress_bar()
        # Start tagline animations
        Clock.schedule_once(self.start_tagline_animation, 1)
    
    def animate_progress_bar(self):
        # Animate progress bar from 0 to 100 over 5 seconds
        progress_anim = Animation(progress_value=100, duration=5)
        progress_anim.bind(on_complete=self.on_progress_complete)
        progress_anim.start(self)
    
    def on_progress_complete(self, *args):
        # Navigate to the main screen when progress bar completes
        print("Loading complete! Navigate to main screen")
        # Add your screen transition code here
        # self.root.current = "main_screen"
    
    def start_tagline_animation(self, dt):
        # Schedule the animation to repeat every 1.25 seconds
        Clock.schedule_interval(self.animate_tagline, 1.25)
    
    def animate_tagline(self, dt):
        # Create fade out animation
        fade_out = Animation(opacity=0, duration=0.3)
        
        # Update the current index
        self.current_index = (self.current_index + 1) % len(self.taglines)
        
        # Define what happens when fade out completes
        def on_complete(animation, widget):
            # Change the tagline text
            self.current_tagline = self.taglines[self.current_index]
            # Create and start fade in animation
            fade_in = Animation(opacity=1, duration=0.3)
            fade_in.start(self.root.get_screen('splash').ids.tagline_label)
        
        # Bind the completion event
        fade_out.bind(on_complete=on_complete)
        # Start the fade out animation
        fade_out.start(self.root.get_screen('splash').ids.tagline_label)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print(f"Switched to: {tab_text}")

    def show_ride_options(self):
        self.dialog = MDDialog(
            title="What would you like to do?",
            type="custom",
            content_cls=RideOptionsDialog(),
        )
        self.dialog.open()

    def show_offer_ride(self):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        self.root.ids.screen_manager.current = "offer_ride"

    def show_request_ride(self):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        self.root.ids.screen_manager.current = "request_ride"

    def go_home(self):
        self.manager.current = "home"

    def show_ride_details(self):
        self.root.ids.screen_manager.current = "ride_details"

    def show_user_profile(self):
        print("Showing user profile")


#popup for scheduling ride
    def show_schedule_popup(self):
        """Show a success popup when a ride is scheduled."""
        self.dialog = MDDialog(
            title=" Ride scheduled Successfully!",
            text="Your ride has been confirmed. Click 'OK' to view details.",
            buttons=[
                MDFlatButton(
                    text="OK", 
                    on_release=self.schedule_details
                )
            ]
        )
        self.dialog.open()

    def schedule_details(self, instance):
        """Close popup and navigate to home screen."""
        self.dialog.dismiss()
        self.root.current = "ride_summary"


#popup for offering ride
    def show_offer_popup(self):
        """Show a success popup when a ride is offered."""
        self.dialog = MDDialog(
            title=" Ride offered Successfully!",
            text="Your ride has been confirmed. Click 'OK' to view details.",
            buttons=[
                MDFlatButton(
                    text="OK", 
                    on_release=self.offer_details
                )
            ]
        )
        self.dialog.open()

    def offer_details(self, instance):
        """Close popup and navigate to home screen."""
        self.dialog.dismiss()
        self.root.current = "ride_summary"




#popup for request ride
    def show_request_popup(self):
        """Show a success popup when a ride is requested."""
        self.dialog = MDDialog(
            title=" Ride requested Successfully!",
            text="Your ride has been confirmed. Click 'OK' to view details.",
            buttons=[
                MDFlatButton(
                    text="OK", 
                    on_release=self.request_details
                )
            ]
        )
        self.dialog.open()

    def request_details(self, instance):
        """Close popup and navigate to ride details screen."""
        self.dialog.dismiss()
        self.root.current = "ride_details"


#Pop-up for booking status 
    def show_success_popup(self):
        """Show a success popup when a ride is booked."""
        self.dialog = MDDialog(
            title=" Ride Booked Successfully!",
            text="Your ride has been confirmed. Click 'OK' to view details.",
            buttons=[
                MDFlatButton(
                    text="OK", 
                    on_release=self.go_to_ride_details
                )
            ]
        )
        self.dialog.open()

    def go_to_ride_details(self, instance):
        """Close popup and navigate to ride details screen."""
        self.dialog.dismiss()
        self.root.current = "ride_summary"


    def load_default_chat(self):
        screen = self.root.get_screen("chatbot")  
        chat_box = screen.ids.chat_box

        default_messages = [
            ("You", "Hi"),
            ("Bot", "Hi, Ride will be reaching the pickup point in 5 mins."),
            
        ]
        
        
        for sender, msg in default_messages:
            chat_box.add_widget(
                MDLabel(
                    text=f"{sender}: {msg}",
                    size_hint_y=None,
                    height=dp(30),
                    theme_text_color="Primary"
                )
            )

# --------------------- Run the App ---------------------

if __name__ == "__main__":
    CarpoolApp().run()
