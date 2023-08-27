from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import pandas as pd

Window.clearcolor = (0, 0, 0, 1)  # Black background color
Window.set_title('PRODUCE PLU LOOKUP TOOL')

class CSVSearcherApp(App):

    def build(self):
        self.df = pd.read_csv('/storage/emulated/0/Documents/Pydroid3/Pydroid3/Pydroid3/Pydroid3/plu_codes.csv', dtype={'PLU Code': 'Int64', 'Name': 'str'})
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Application title
        header_label = Label(text='PRODUCE PLU LOOKUP TOOL', font_size=50, color=(1, 1, 1, 1))
        layout.add_widget(header_label)
        
        # Search bar
        self.search_input = TextInput(hint_text='Search...', multiline=False, size_hint_y=0.15, font_size=45, cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1), background_color=(0.5, 0.5, 0.5, 1)) # Medium gray background
        self.search_input.bind(text=self.on_text)
        layout.add_widget(self.search_input)
        
        # Output window
        self.output_label = Label(size_hint_y=None, font_size=45, color=(1, 1, 1, 1))
        self.output_label.bind(width=lambda *x: self.output_label.setter('text_size')(self.output_label, (self.output_label.width, None)))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.output_label)
        layout.add_widget(scroll_view)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=0.15)
        clear_button = Button(text='Clear', font_size=45, on_press=self.clear_search)
        exit_button = Button(text='Exit', font_size=45, on_press=self.exit_app)
        button_layout.add_widget(clear_button)
        button_layout.add_widget(exit_button)
        layout.add_widget(button_layout)
        
        # Creator's name
        creator_label = Label(text='Created by Brian Askew', font_size=33, color=(1, 1, 5, 5))
        layout.add_widget(creator_label)
        
        return layout

    def on_text(self, instance, value):
        search_for = value.strip()
        if search_for:
            results = self.df[(self.df['Name'].astype(str).str.contains(search_for, case=False)) | (self.df['PLU Code'].astype(str).str.contains(search_for, case=False))]
            results_str = '\n'.join([f"{row['PLU Code']} - {row['Name']}" for _, row in results.iterrows()])
            self.output_label.text = results_str
        else:
            self.output_label.text = ''

    def clear_search(self, instance):
        self.search_input.text = ''
        self.output_label.text = ''

    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    CSVSearcherApp().run()
