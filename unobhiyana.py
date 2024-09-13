import sys
import requests  # For making the API requests
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, 
    QWidget, QComboBox, QTabWidget, QPlainTextEdit, QToolTip
)
from qtpy.QtCore import Qt

# Google API Key and CSE ID - replace with your own values
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
GOOGLE_CSE_ID = 'YOUR_CUSTOM_SEARCH_ENGINE_ID'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle('Unobhiyana-ka-Madondo')
        self.setGeometry(200, 200, 900, 700)
        
        # Apply a dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel, QPlainTextEdit {
                color: white;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #333;
                border-radius: 8px;
                background-color: #222;
                color: white;
                margin-bottom: 10px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #3a3a3a;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QTabWidget::pane {
                border: 1px solid #333;
                background: #1f1f1f;
                border-radius: 8px;
            }
            QPlainTextEdit {
                background-color: #222;
                border-radius: 8px;
                border: 1px solid #333;
                color: white;
            }
        """)

        # Create tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_search_tab(), "Search")
        tabs.addTab(self.create_suppression_tab(), "Suppression")
        tabs.addTab(self.create_tracking_tab(), "Tracking")
        
        # Set the central widget
        self.setCentralWidget(tabs)

    def create_search_tab(self):
        """Create the Search tab."""
        search_tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("User Data Search Inputs"))
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP Address (e.g., 192.168.0.1)")
        layout.addWidget(self.ip_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        layout.addWidget(self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        layout.addWidget(self.email_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Social Media Username")
        layout.addWidget(self.username_input)
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Physical Address")
        layout.addWidget(self.address_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_input)
        
        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("Number Plate")
        layout.addWidget(self.plate_input)

        # Search button and Clear button
        search_button = QPushButton("Search Data")
        search_button.clicked.connect(self.search_data)  # Connect button to search function
        clear_button = QPushButton("Clear Inputs")
        clear_button.clicked.connect(self.clear_inputs)  # Connect button to clear inputs
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        self.search_results = QPlainTextEdit()
        self.search_results.setPlaceholderText("Search results will appear here...")
        layout.addWidget(self.search_results)

        search_tab.setLayout(layout)
        return search_tab

    def create_suppression_tab(self):
        """Create the Suppression tab."""
        suppression_tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Select Suppression Method"))
        
        self.suppression_method = QComboBox()
        self.suppression_method.addItems([
            "Legal Takedown (DMCA)",
            "Right to Be Forgotten (EU Jurisdictions)",
            "Direct Website Contact",
            "Google Search Console (Outdated Content)",
            "SEO Suppression",
            "Temporary Suppression (PPC Ads)",
            "Deindexing (Google Search Console)"
        ])
        layout.addWidget(self.suppression_method)

        layout.addWidget(QLabel("Manual Input for Suppression:"))
        self.manual_input_area = QPlainTextEdit()
        self.manual_input_area.setPlaceholderText("Enter the details for the selected suppression method (e.g., legal reasons, SEO keywords).")
        layout.addWidget(self.manual_input_area)

        # AI suggestions button (if enabled later)
        ai_suggestions_button = QPushButton("Get AI Suggestions")
        layout.addWidget(ai_suggestions_button)
        
        self.submit_button = QPushButton("Submit Suppression Request")
        self.submit_button.clicked.connect(self.execute_process)
        layout.addWidget(self.submit_button)
        
        suppression_tab.setLayout(layout)
        return suppression_tab
    
    def create_tracking_tab(self):
        """Create the Tracking tab."""
        tracking_tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Track Suppression Progress"))
        self.track_area = QPlainTextEdit()
        self.track_area.setPlaceholderText("Track the progress of suppression requests here...")
        self.track_area.setReadOnly(True)
        layout.addWidget(self.track_area)
        
        self.refresh_button = QPushButton("Refresh Progress")
        self.refresh_button.clicked.connect(self.refresh_progress)
        layout.addWidget(self.refresh_button)
        
        tracking_tab.setLayout(layout)
        return tracking_tab
    
    def execute_process(self):
        """Simulate submission of suppression request."""
        method = self.suppression_method.currentText()
        manual_input = self.manual_input_area.toPlainText()

        # Log submission
        self.track_area.appendPlainText(f"Submitted suppression method: {method}")
        self.track_area.appendPlainText(f"Details: {manual_input}\n")
    
    def refresh_progress(self):
        """Simulate refreshing of progress."""
        # Simulate updating the log area
        self.track_area.appendPlainText("Progress refreshed: No new updates.")

    def search_data(self):
        """Perform a Google Custom Search using the API."""
        query = self.name_input.text() or self.email_input.text() or self.username_input.text()

        if not query:
            self.search_results.setPlainText("Please enter a name, email, or username to search.")
            return

        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={query}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if 'items' in data:
                results = "\n".join([f"Title: {item['title']}\nLink: {item['link']}\n" for item in data['items']])
                self.search_results.setPlainText(results)
            else:
                self.search_results.setPlainText("No results found.")
        except Exception as e:
            self.search_results.setPlainText(f"Error fetching data: {e}")

    def clear_inputs(self):
        """Clear all input fields."""
        self.ip_input.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.username_input.clear()
        self.address_input.clear()
        self.phone_input.clear()
        self.plate_input.clear()
        self.search_results.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
