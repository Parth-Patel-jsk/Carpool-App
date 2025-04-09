from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

def close_dialog(self, instance):
    self.dialog.dismiss()

def reload_signup_screen(self, instance):
    self.close_dialog(instance)
    screen_manager = self.root
    if 'register' in screen_manager.screen_names:
        register_screen = screen_manager.get_screen('register')
        if hasattr(self, 'saved_new_email'):
            register_screen.ids.new_email.text = self.saved_new_email
        if hasattr(self, 'saved_new_password'):
            register_screen.ids.new_password.text = self.saved_new_password

        # Clear the saved data
        self.saved_new_email = ""
        self.saved_new_password = ""
        screen_manager.current ='register'
    else:
        print("Register screen not found in ScreenManager")
def reload_login_screen(self, instance):
    self.close_dialog(instance)
    screen_manager = self.root
    login_screen = screen_manager.get_screen('login')

    # Restore saved email and password
    if self.saved_email:
        login_screen.ids.email.text = self.saved_email
    if self.saved_password:
        login_screen.ids.password.text = self.saved_password

    # Clear the saved data
    self.saved_email = ""
    self.saved_password = ""
    screen_manager.current = 'login'

def show_missing_dialog(self, message):
    self.dialog = MDDialog(
        title="Error",
        text=message,
        size_hint=(0.7, 1),
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=self.reload_current_screen
            )
        ]
    )
    self.dialog.shadow_color = [0, 0, 0, 0]
    self.dialog.open()

def show_already_registered_dialog(self):
    self.dialog = MDDialog(
        title="Email Already Registered",
        text="This email is already registered. Please use a different email.",
        size_hint=(0.5, 1),
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=self.reload_signup_screen
            )
        ]
    )
    self.dialog.shadow_color = [0, 0, 0, 0]
    self.dialog.open()

def reload_current_screen(self, instance):
    self.close_dialog(instance)
    screen_manager = self.root
    current_screen = screen_manager.current

    if current_screen == 'register':
        self.reload_signup_screen(instance)
    elif current_screen == 'login':
        self.reload_login_screen(instance)
def show_error_email_format(self, message):
        self.dialog = MDDialog(
                text=message,
                buttons=[MDRaisedButton(text="OK", on_release=self.reload_current_screen)]
        )
        self.dialog.shadow_color = [0, 0, 0, 0]
        self.dialog.open()

def handle_successful_signup(self):
    screen_manager = self.root
    register_screen = screen_manager.get_screen('register')

    # Clear data in the signup screen
    register_screen.ids.new_username.text = ""
    register_screen.ids.new_licence.text = ""
    register_screen.ids.new_email.text = ""
    register_screen.ids.new_password.text = ""

    # Redirect to otp  screen
    screen_manager.current = 'otp'

def show_wrong_password(self,message):
    self.dialog = MDDialog(
        title="Error",
        text=message,
        size_hint=(0.7, 1),
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=lambda x: self.dialog.dismiss()
            )
        ]
    )
    self.dialog.shadow_color = [0, 0, 0, 0]
    self.dialog.open()
def show_wrong_password_email(self,message):
    self.dialog = MDDialog(
        title="Error",
        text=message,
        size_hint=(0.7, 1),
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=lambda x: self.dialog.dismiss()
            )
        ]
    )
    self.dialog.shadow_color = [0, 0, 0, 0]
    self.dialog.open()
def reload_main_screen(self, instance):
    self.close_dialog(instance)
    screen_manager = self.root
    if 'main' in screen_manager.screen_names:
        main_screen = screen_manager.get_screen('main')
        self.saved_new_username=""
        self.saved_new_licence=""
        # Clear the saved data
        self.saved_new_email = ""
        self.saved_new_password= ""
        screen_manager.current = 'main'
    else:
        print("Signup screen not found in ScreenManager")

def show_wrong_otp(self,message):
    self.dialog = MDDialog(
        title="Error",
        text=message,
        size_hint=(0.7, 1),
        buttons=[
            MDRaisedButton(
                text="OK",
                on_release=self.reload_main_screen
            )
        ]
    )
    self.dialog.shadow_color = [0, 0, 0, 0]
    self.dialog.open()
