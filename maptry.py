from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarker
from kivy.clock import Clock
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import threading
import certifi
import ssl
import os

# Configure SSL context for geopy
ctx = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent="navigation_app", ssl_context=ctx)

KV = '''
#:import MapView kivy_garden.mapview.MapView

<DestinationScreen>:
    mapview: mapview  # Create a direct reference to the MapView
    destination_input: destination_input  # Direct reference to TextInput
    
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint: 1, 0.12
            pos_hint: {"top": 1}
            canvas.before:
                Color:
                    rgba: 0.13, 0.59, 0.95, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Label:
                text: "Navigation App"
                color: 1, 1, 1, 1
                font_size: "20sp"
                bold: True
                halign: "center"
                valign: "middle"

        BoxLayout:
            orientation: "vertical"
            size_hint: 0.9, 0.15
            pos_hint: {"center_x": 0.5, "top": 0.88}
            padding: [10, 0]
            spacing: 5

            TextInput:
                id: destination_input
                hint_text: "Enter destination address"
                size_hint_y: 0.6
                multiline: False
                font_size: "16sp"
                background_color: 1, 1, 1, 1
                foreground_color: 0, 0, 0, 1
                hint_text_color: 0.5, 0.5, 0.5, 1
                padding: [10, 10]
                write_tab: False
                on_text_validate: root.navigate_to_destination()
                canvas.before:
                    Color:
                        rgba: 0.13, 0.59, 0.95, 1
                    Line:
                        width: 1.5
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

        MapView:
            id: mapview
            size_hint: 0.95, 0.6
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            zoom: 12
            lat: 40.7128  # New York
            lon: -74.0060

        BoxLayout:
            orientation: "horizontal"
            size_hint: 0.9, 0.1
            pos_hint: {"center_x": 0.5, "y": 0.05}
            spacing: 10
            
            Button:
                text: "Navigate"
                background_color: 0.13, 0.59, 0.95, 1
                background_normal: ''
                color: 1, 1, 1, 1
                font_size: "16sp"
                bold: True
                on_release: root.navigate_to_destination()
                
            Button:
                text: "Reset"
                background_color: 0.9, 0.1, 0.1, 1
                background_normal: ''
                color: 1, 1, 1, 1
                font_size: "16sp"
                on_release: root.reset_map()
'''

class DestinationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marker = None
        self.default_lat = 40.7128
        self.default_lon = -74.0060
        self.default_zoom = 12
        self.map_initialized = False
        Clock.schedule_once(self.initialize_map, 1)
    
    def initialize_map(self, dt):
        """Initialize map after widgets are fully loaded"""
        if not self.map_initialized and hasattr(self, 'mapview'):
            try:
                # Create a default marker
                marker_path = os.path.join(os.path.dirname(__file__), "marker.png")
                if not os.path.exists(marker_path):
                    print(f"Marker image not found at: {marker_path}")
                    # Create a simple marker if file doesn't exist
                    self.marker = MapMarker(lat=self.default_lat, lon=self.default_lon)
                else:
                    self.marker = MapMarker(
                        lat=self.default_lat,
                        lon=self.default_lon,
                        source=marker_path
                    )
                
                self.mapview.add_marker(self.marker)
                self.map_initialized = True
            except Exception as e:
                print(f"Map initialization error: {e}")
                Clock.schedule_once(self.initialize_map, 0.5)
    
    def on_enter(self, *args):
        """Ensure map is ready when screen is shown"""
        if not self.map_initialized:
            self.initialize_map(0)
    
    def navigate_to_destination(self):
        """Handle navigation button press"""
        if not hasattr(self, 'destination_input'):
            print("Destination input not available yet")
            return
            
        address = self.destination_input.text.strip()
        if not address:
            self.show_error("Please enter an address")
            return
            
        self.destination_input.disabled = True
        self.destination_input.hint_text = "Searching..."
        self.destination_input.text = ""
        
        threading.Thread(
            target=self.geocode_address,
            args=(address,),
            daemon=True
        ).start()
    
    def geocode_address(self, address):
        """Convert address to coordinates"""
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                Clock.schedule_once(
                    lambda dt: self.update_map(location.latitude, location.longitude)
                )
            else:
                Clock.schedule_once(
                    lambda dt: self.show_error("Location not found")
                )
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            Clock.schedule_once(
                lambda dt: self.show_error("Network error. Try again.")
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            Clock.schedule_once(
                lambda dt: self.show_error("An error occurred")
            )
        finally:
            if hasattr(self, 'destination_input'):
                Clock.schedule_once(
                    lambda dt: setattr(self.destination_input, 'disabled', False)
                )
    
    def update_map(self, lat, lon):
        """Update map with new coordinates"""
        if not hasattr(self, 'mapview') or not self.marker:
            print("Map not ready for update")
            return
            
        try:
            self.marker.lat = lat
            self.marker.lon = lon
            self.mapview.center_on(lat, lon)
            self.destination_input.hint_text = "Enter destination address"
        except Exception as e:
            print(f"Error updating map: {e}")
            self.show_error("Failed to update map")
    
    def reset_map(self):
        """Reset map to default location"""
        if not hasattr(self, 'mapview') or not self.marker:
            return
            
        try:
            self.mapview.center_on(self.default_lat, self.default_lon)
            self.mapview.zoom = self.default_zoom
            self.marker.lat = self.default_lat
            self.marker.lon = self.default_lon
            self.destination_input.text = ""
            self.destination_input.hint_text = "Enter destination address"
        except Exception as e:
            print(f"Error resetting map: {e}")
    
    def show_error(self, message):
        """Display error message"""
        if hasattr(self, 'destination_input'):
            self.destination_input.hint_text = message
            self.destination_input.text = ""

class NavigationApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    NavigationApp().run()