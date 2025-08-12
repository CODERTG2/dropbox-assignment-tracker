import os
import json
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTextEdit, QLineEdit, 
                           QMessageBox, QTabWidget, QWidget, QFrame,
                           QScrollArea, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class WelcomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment Tracker Setup")
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.setup_ui()
        self.apply_styling()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Welcome header
        welcome_label = QLabel("Welcome to Assignment Tracker")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        subtitle = QLabel("Let's set up your Google Sheets integration")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Instructions frame
        instructions_frame = QFrame()
        instructions_frame.setFrameStyle(QFrame.Box)
        instructions_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        instructions_layout = QVBoxLayout()
        
        instructions_title = QLabel("What you'll need:")
        instructions_title.setFont(QFont("Arial", 16, QFont.Bold))
        instructions_layout.addWidget(instructions_title)
        
        steps = [
            "1. Google Sheets API credentials (JSON file or content)",
            "2. Your Google Sheets ID",
            "3. About 2 minutes to complete setup"
        ]
        
        for step in steps:
            step_label = QLabel(step)
            step_label.setFont(QFont("Arial", 12))
            step_label.setStyleSheet("margin: 5px 0px; padding-left: 10px;")
            instructions_layout.addWidget(step_label)
        
        instructions_frame.setLayout(instructions_layout)
        layout.addWidget(instructions_frame)
        
        # Help button
        help_button = QPushButton("Need Help Getting Credentials?")
        help_button.clicked.connect(self.show_help)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        layout.addWidget(help_button)
        
        layout.addStretch()
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.continue_button = QPushButton("Continue Setup")
        self.continue_button.clicked.connect(self.accept)
        self.continue_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 12px 30px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 12px 30px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.continue_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def apply_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLabel {
                color: #333;
            }
        """)
    
    def show_help(self):
        help_dialog = CredentialsHelpDialog(self)
        help_dialog.exec_()

class CredentialsHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("How to Get Google Sheets Credentials")
        self.setFixedSize(700, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Scrollable content
        scroll = QScrollArea()
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        title = QLabel("Getting Google Sheets API Credentials")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        content_layout.addWidget(title)
        
        help_text = """
        <div style="font-size: 14px; line-height: 1.6;">
        
        <h3 style="color: #28a745;">Step 1: Go to Google Cloud Console</h3>
        <p>1. Visit <a href="https://console.cloud.google.com/">console.cloud.google.com</a></p>
        <p>2. Create a new project or select an existing one</p>
        
        <h3 style="color: #28a745;">Step 2: Enable Google Sheets API</h3>
        <p>1. Go to "APIs & Services" → "Library"</p>
        <p>2. Search for "Google Sheets API"</p>
        <p>3. Click "Enable"</p>
        
        <h3 style="color: #28a745;">Step 3: Create Credentials</h3>
        <p>1. Go to "APIs & Services" → "Credentials"</p>
        <p>2. Click "Create Credentials" → "Service Account"</p>
        <p>3. Fill in the service account details</p>
        <p>4. Click "Create and Continue"</p>
        <p>5. Skip optional steps and click "Done"</p>
        
        <h3 style="color: #28a745;">Step 4: Download Key File</h3>
        <p>1. Click on your service account email</p>
        <p>2. Go to "Keys" tab</p>
        <p>3. Click "Add Key" → "Create new key"</p>
        <p>4. Choose "JSON" format</p>
        <p>5. Download the file</p>
        
        <h3 style="color: #28a745;">Step 5: Get Sheet ID</h3>
        <p>From your Google Sheets URL:</p>
        <p><code>https://docs.google.com/spreadsheets/d/<strong>SHEET_ID_HERE</strong>/edit</code></p>
        
        <h3 style="color: #dc3545;">Step 6: Share Your Sheet</h3>
        <p><strong>Important:</strong> Share your Google Sheet with the service account email address (found in the JSON file) with "Editor" permissions.</p>
        
        </div>
        """
        
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setOpenExternalLinks(True)
        content_layout.addWidget(help_label)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Close button
        close_button = QPushButton("Got it!")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 30px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)

class CredentialsSetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Credentials")
        self.setFixedSize(700, 600)
        self.setModal(True)
        self.setup_ui()
        self.apply_styling()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Enter Your Credentials")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tabs for different input methods
        tabs = QTabWidget()
        
        # Tab 1: Paste JSON content
        paste_tab = QWidget()
        paste_layout = QVBoxLayout()
        
        paste_instructions = QLabel("Paste the contents of your credentials.json file:")
        paste_instructions.setFont(QFont("Arial", 12, QFont.Bold))
        paste_layout.addWidget(paste_instructions)
        
        self.credentials_text = QTextEdit()
        self.credentials_text.setPlaceholderText('''Paste your JSON credentials here, for example:
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}''')
        self.credentials_text.setFont(QFont("Monaco", 10))
        self.credentials_text.setMinimumHeight(200)
        paste_layout.addWidget(self.credentials_text)
        
        paste_tab.setLayout(paste_layout)
        tabs.addTab(paste_tab, "Paste JSON")
        
        # Tab 2: Upload file (placeholder for future implementation)
        upload_tab = QWidget()
        upload_layout = QVBoxLayout()
        upload_layout.addWidget(QLabel("File upload feature coming soon!"))
        upload_layout.addWidget(QLabel("For now, please use the 'Paste JSON' tab."))
        upload_tab.setLayout(upload_layout)
        tabs.addTab(upload_tab, "Upload File")
        
        layout.addWidget(tabs)
        
        # Sheet ID input
        sheet_layout = QVBoxLayout()
        sheet_label = QLabel("Google Sheets ID:")
        sheet_label.setFont(QFont("Arial", 12, QFont.Bold))
        sheet_layout.addWidget(sheet_label)
        
        self.sheet_id_input = QLineEdit()
        self.sheet_id_input.setPlaceholderText("Paste your Sheet ID here (found in the Google Sheets URL)")
        self.sheet_id_input.setFont(QFont("Arial", 11))
        sheet_layout.addWidget(self.sheet_id_input)
        
        hint_label = QLabel("Tip: The Sheet ID is the long string in your Google Sheets URL")
        hint_label.setStyleSheet("color: #666; font-style: italic; margin-top: 5px;")
        sheet_layout.addWidget(hint_label)
        
        layout.addLayout(sheet_layout)
        
        # Test connection checkbox
        self.test_connection = QCheckBox("Test connection before saving")
        self.test_connection.setChecked(True)
        layout.addWidget(self.test_connection)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 12px 30px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        button_layout.addWidget(back_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def apply_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLabel {
                color: #333;
            }
            QTextEdit, QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
            QTextEdit:focus, QLineEdit:focus {
                border-color: #28a745;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: none;
            }
        """)
    
    def save_configuration(self):
        try:
            # Validate JSON
            credentials_text = self.credentials_text.toPlainText().strip()
            sheet_id = self.sheet_id_input.text().strip()
            
            if not credentials_text:
                QMessageBox.warning(self, "Error", "Please enter your credentials JSON")
                return
            
            if not sheet_id:
                QMessageBox.warning(self, "Error", "Please enter your Sheet ID")
                return
            
            # Validate JSON format
            try:
                credentials_data = json.loads(credentials_text)
                required_fields = ['type', 'client_email', 'private_key']
                missing_fields = [field for field in required_fields if field not in credentials_data]
                if missing_fields:
                    QMessageBox.warning(self, "Invalid JSON", 
                                      f"Missing required fields: {', '.join(missing_fields)}")
                    return
            except json.JSONDecodeError as e:
                QMessageBox.critical(self, "Invalid JSON", 
                                   f"Invalid JSON format:\n{str(e)}")
                return
            
            # Test connection if requested
            if self.test_connection.isChecked():
                self.save_button.setText("Testing connection...")
                self.save_button.setEnabled(False)
                QApplication.processEvents()
                
                # Test the connection by trying to create a SheetReader
                try:
                    # Write temporary credentials file
                    temp_creds_path = "temp_credentials.json"
                    with open(temp_creds_path, 'w') as f:
                        f.write(credentials_text)
                    
                    # Try to initialize SheetReader
                    from SheetReader import SheetReader
                    test_reader = SheetReader(temp_creds_path, sheet_id)
                    
                    # Try to get assignments (this will test the connection)
                    assignments = test_reader.get_assignments()
                    
                    # Clean up temp file
                    os.remove(temp_creds_path)
                    
                    QMessageBox.information(self, "Connection Test", 
                        f"Connection successful!\nFound {len(assignments)} assignments in your sheet.")
                    
                except Exception as e:
                    # Clean up temp file if it exists
                    if os.path.exists(temp_creds_path):
                        os.remove(temp_creds_path)
                    
                    QMessageBox.critical(self, "Connection Test Failed", 
                        f"Could not connect to your Google Sheet:\n\n{str(e)}\n\n"
                        "Please check:\n"
                        "• Your credentials are correct\n"
                        "• Your Sheet ID is correct\n"
                        "• You've shared the sheet with your service account email")
                    
                    self.save_button.setText("Save Configuration")
                    self.save_button.setEnabled(True)
                    return
                
                self.save_button.setText("Save Configuration")
                self.save_button.setEnabled(True)
            
            # Save to config directory
            config_dir = os.path.expanduser("~/.assignment_tracker")
            os.makedirs(config_dir, exist_ok=True)
            
            # Save credentials
            with open(os.path.join(config_dir, "credentials.json"), 'w') as f:
                f.write(credentials_text)
            
            # Save .env file
            with open(os.path.join(config_dir, ".env"), 'w') as f:
                f.write(f"SHEET_ID={sheet_id}\n")
            
            QMessageBox.information(self, "Success", 
                f"Configuration saved successfully!\n\nFiles saved to:\n{config_dir}")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{str(e)}")

def run_setup_wizard():
    """Run the complete setup wizard"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
    
    # Show welcome screen
    welcome = WelcomeScreen()
    if welcome.exec_() != QDialog.Accepted:
        return False
    
    # Show credentials setup
    credentials_setup = CredentialsSetupDialog()
    return credentials_setup.exec_() == QDialog.Accepted

if __name__ == "__main__":
    success = run_setup_wizard()
    if success:
        print("Setup completed successfully!")
    else:
        print("Setup cancelled.")
