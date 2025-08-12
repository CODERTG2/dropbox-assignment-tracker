from SheetReader import SheetReader
import os
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QPushButton, QTextEdit, QComboBox, 
                           QLineEdit, QRadioButton, QButtonGroup, QFrame, 
                           QScrollArea, QMessageBox, QProgressBar, QSizePolicy, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from dotenv import load_dotenv
from setup_wizard import run_setup_wizard

class LoadAssignmentsThread(QThread):
    """Thread for loading assignments to prevent UI blocking"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, sheet_reader):
        super().__init__()
        self.sheet_reader = sheet_reader
    
    def run(self):
        try:
            assignments = self.sheet_reader.get_assignments()
            self.finished.emit(assignments)
        except Exception as e:
            self.error.emit(str(e))

class AssignmentTrackerApp(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = file_path
        self.current_assignment = None
        self.is_updating = False
        
        # Check for configuration first
        if not self.check_configuration():
            return
            
        self.setup_ui()
        self.setup_clients()
        self.apply_modern_styling()
    
    def check_configuration(self):
        """Check if configuration exists, run setup wizard if not"""
        config_dir = os.path.expanduser("~/.assignment_tracker")
        creds_path = os.path.join(config_dir, "credentials.json")
        env_path = os.path.join(config_dir, ".env")
        
        if not os.path.exists(creds_path) or not os.path.exists(env_path):
            if not run_setup_wizard():
                QMessageBox.information(None, "Setup Required", 
                    "Setup is required to use Assignment Tracker.")
                sys.exit(0)
        
        # Load environment from config directory
        load_dotenv(env_path)
        self.credentials_path = creds_path
        return True
    
    def setup_ui(self):
        self.setWindowTitle("Assignment Tracker")
        self.setGeometry(100, 100, 600, 280)  # Much smaller height
        self.setMinimumSize(500, 250)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Assignment Tracker")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        if self.file_path:
            file_label = QLabel(f"File: {os.path.basename(self.file_path)}")
            file_label.setFont(QFont("Arial", 10))
            file_label.setStyleSheet("color: #666;")
            header_layout.addWidget(file_label)
        
        # Add settings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        header_layout.addWidget(settings_button)
        
        main_layout.addLayout(header_layout)
        
        # Assignment selection section
        selection_label = QLabel("Select Assignment:")
        selection_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(selection_label)
        
        # Dropdown and search layout
        dropdown_layout = QHBoxLayout()
        self.assignment_dropdown = QComboBox()
        self.assignment_dropdown.setEditable(True)
        self.assignment_dropdown.setPlaceholderText("Search or select an assignment...")
        self.assignment_dropdown.currentTextChanged.connect(self.on_assignment_changed)
        
        self.search_button = QPushButton("Load Assignment")
        self.search_button.clicked.connect(self.load_assignment_details)
        self.search_button.setEnabled(False)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_assignment)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        dropdown_layout.addWidget(self.assignment_dropdown, 3)
        dropdown_layout.addWidget(self.search_button, 1)
        dropdown_layout.addWidget(self.clear_button, 0)
        main_layout.addLayout(dropdown_layout)
        
        # Loading indicator
        self.loading_bar = QProgressBar()
        self.loading_bar.setVisible(False)
        main_layout.addWidget(self.loading_bar)
        
        # Assignment details section
        self.details_frame = QFrame()
        self.details_frame.setVisible(False)
        self.setup_details_section()
        main_layout.addWidget(self.details_frame)
        
        # Status section
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(60)  # Even smaller initially
        self.status_text.setPlaceholderText("Status updates will appear here...")
        main_layout.addWidget(self.status_text)
        
        central_widget.setLayout(main_layout)
    
    def setup_details_section(self):
        details_layout = QVBoxLayout()
        
        details_title = QLabel("Assignment Details")
        details_title.setFont(QFont("Arial", 12, QFont.Bold))
        details_layout.addWidget(details_title)
        
        # Create a scroll area for the form
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        form_layout = QVBoxLayout()
        
        # Description field
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(desc_label)
        self.description_field = QTextEdit()
        self.description_field.setMaximumHeight(80)
        self.description_field.setPlaceholderText("Enter assignment description...")
        form_layout.addWidget(self.description_field)
        
        # Due date field
        date_label = QLabel("Due Date:")
        date_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(date_label)
        self.due_date_field = QLineEdit()
        self.due_date_field.setPlaceholderText("YYYY-MM-DD or any date format...")
        form_layout.addWidget(self.due_date_field)
        
        # Progress radio buttons
        progress_label = QLabel("Progress:")
        progress_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(progress_label)
        
        progress_layout = QHBoxLayout()
        self.progress_group = QButtonGroup()
        
        self.not_started_radio = QRadioButton("Not Started")
        self.wip_radio = QRadioButton("In Progress") 
        self.done_radio = QRadioButton("Completed")
        
        self.progress_group.addButton(self.not_started_radio, 0)
        self.progress_group.addButton(self.wip_radio, 1)
        self.progress_group.addButton(self.done_radio, 2)
        
        progress_layout.addWidget(self.not_started_radio)
        progress_layout.addWidget(self.wip_radio)
        progress_layout.addWidget(self.done_radio)
        progress_layout.addStretch()
        
        form_layout.addLayout(progress_layout)
        
        # Assignee field
        assignee_label = QLabel("Assignee:")
        assignee_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(assignee_label)
        self.assignee_field = QLineEdit()
        self.assignee_field.setPlaceholderText("Enter assignee name...")
        form_layout.addWidget(self.assignee_field)
        
        # Save button
        form_layout.addWidget(QLabel())  # Add some spacing
        self.save_button = QPushButton("Save Assignment")
        self.save_button.clicked.connect(self.save_assignment)
        form_layout.addWidget(self.save_button)
        
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        details_layout.addWidget(scroll_area)
        
        self.details_frame.setLayout(details_layout)
    
    def apply_modern_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            QLabel {
                color: #333;
            }
            
            QComboBox {
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            
            QComboBox:focus {
                border-color: #4CAF50;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-weight: bold;
                border-radius: 4px;
                font-size: 11px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #999;
            }
            
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            
            QTextEdit:focus {
                border-color: #4CAF50;
            }
            
            QRadioButton {
                font-size: 12px;
                color: #333;
                spacing: 8px;
                margin-right: 20px;
                padding: 4px;
            }
            
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 4px;
                text-align: center;
                font-size: 12px;
                background-color: #f0f0f0;
                min-height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 2px;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #ccc;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #aaa;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
    
    def setup_clients(self):
        try:
            self.status_text.append("Initializing clients...")
            self.sheet_reader = SheetReader(self.credentials_path, os.getenv("SHEET_ID"))
            self.status_text.append("Clients initialized successfully")
            self.load_assignments()
        except Exception as e:
            self.status_text.append(f"Error initializing clients: {str(e)}")
            QMessageBox.critical(self, "Configuration Error", 
                f"Failed to initialize Google Sheets connection:\n{str(e)}\n\n"
                "Please check your credentials and try again.")
            sys.exit(1)
    
    def load_assignments(self):
        """Load assignments in a separate thread"""
        self.loading_bar.setVisible(True)
        self.loading_bar.setRange(0, 0)  # Indeterminate progress
        self.status_text.append("Loading assignments from spreadsheet...")
        
        self.assignment_thread = LoadAssignmentsThread(self.sheet_reader)
        self.assignment_thread.finished.connect(self.on_assignments_loaded)
        self.assignment_thread.error.connect(self.on_assignments_error)
        self.assignment_thread.start()
    
    def on_assignments_loaded(self, assignments):
        """Handle successful assignment loading"""
        self.loading_bar.setVisible(False)
        self.assignment_dropdown.clear()
        self.assignment_dropdown.addItems(assignments)
        self.status_text.append(f"Loaded {len(assignments)} assignments")
        self.search_button.setEnabled(True)
    
    def on_assignments_error(self, error_msg):
        """Handle assignment loading error"""
        self.loading_bar.setVisible(False)
        self.status_text.append(f"Error loading assignments: {error_msg}")
        QMessageBox.critical(self, "Error", f"Failed to load assignments:\n{error_msg}")
    
    def on_assignment_changed(self):
        """Handle assignment dropdown change"""
        current_text = self.assignment_dropdown.currentText().strip()
        self.search_button.setEnabled(bool(current_text))
    
    def clear_assignment(self):
        """Clear the current assignment and hide details"""
        self.assignment_dropdown.setCurrentText("")
        self.details_frame.setVisible(False)
        self.current_assignment = None
        # Resize back to compact size
        self.resize(600, 280)
        # Shrink status area back
        self.status_text.setMaximumHeight(60)
        self.status_text.append("Cleared assignment selection")
    
    def load_assignment_details(self):
        """Load details for the selected assignment"""
        assignment = self.assignment_dropdown.currentText().strip()
        if not assignment:
            return
        
        self.current_assignment = assignment
        self.status_text.append(f"Loading details for: {assignment}")
        
        try:
            # Load assignment details
            description = self.sheet_reader.get_description(assignment) or ""
            due_date = self.sheet_reader.get_due_date(assignment) or ""
            progress = self.sheet_reader.get_progress(assignment) or ""
            assignee = self.sheet_reader.get_assignee(assignment) or ""
            
            # Populate fields
            self.description_field.setPlainText(description)
            self.due_date_field.setText(due_date)
            self.assignee_field.setText(assignee)
            
            # Set progress radio button
            self.progress_group.setExclusive(False)  # Temporarily disable exclusivity
            self.not_started_radio.setChecked(False)
            self.wip_radio.setChecked(False)
            self.done_radio.setChecked(False)
            self.progress_group.setExclusive(True)  # Re-enable exclusivity
            
            if progress.lower() in ['not started', 'not_started', '']:
                self.not_started_radio.setChecked(True)
            elif progress.lower() in ['wip', 'work in progress', 'in progress']:
                self.wip_radio.setChecked(True)
            elif progress.lower() in ['done', 'completed', 'finished']:
                self.done_radio.setChecked(True)
            
            # Check if this is an update (assignment exists) or new assignment
            existing_assignments = self.sheet_reader.get_assignments()
            self.is_updating = assignment in existing_assignments
            
            # Show details section and resize window
            self.details_frame.setVisible(True)
            # Expand window to accommodate details
            self.resize(700, 650)
            # Expand status area too
            self.status_text.setMaximumHeight(120)
            self.status_text.append(f"Loaded details for {assignment}")
            
        except Exception as e:
            self.status_text.append(f"Error loading assignment details: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load assignment details:\n{str(e)}")
    
    def save_assignment(self):
        """Save the assignment data"""
        if not self.current_assignment:
            QMessageBox.warning(self, "Warning", "No assignment selected")
            return
        
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "No file path specified")
            return
        
        try:
            # Get form data
            description = self.description_field.toPlainText().strip()
            due_date = self.due_date_field.text().strip()
            assignee = self.assignee_field.text().strip()
            
            # Get progress from radio buttons
            progress = ""
            if self.not_started_radio.isChecked():
                progress = "Not Started"
            elif self.wip_radio.isChecked():
                progress = "WIP"
            elif self.done_radio.isChecked():
                progress = "Done"
            
            self.status_text.append(f"Saving assignment: {self.current_assignment}")
            
            # Update spreadsheet
            self.sheet_reader.update_record(
                assignment=self.current_assignment,
                file_path=self.file_path,
                description=description,
                due_date=due_date,
                progress=progress,
                assignee=assignee
            )
            
            self.status_text.append(f"Successfully saved assignment: {self.current_assignment}")
            QMessageBox.information(self, "Success", f"Assignment '{self.current_assignment}' saved successfully!")
            
        except Exception as e:
            error_msg = f"Failed to save assignment: {str(e)}"
            self.status_text.append(f"{error_msg}")
            QMessageBox.critical(self, "Error", error_msg)
    
    def open_settings(self):
        """Open settings dialog to reconfigure credentials"""
        reply = QMessageBox.question(self, "Reconfigure Settings", 
            "Do you want to reconfigure your Google Sheets credentials?\n\n"
            "This will replace your current configuration.",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if run_setup_wizard():
                QMessageBox.information(self, "Settings Updated", 
                    "Settings updated successfully! Please restart the application for changes to take effect.")
                sys.exit(0)

def main():
    app = QApplication(sys.argv)
    
    # Set application properties for better styling
    app.setStyle('Fusion')
    
    # Get file path from command line arguments
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Processing file: {file_path}")
    else:
        print("No file specified via command line")

    window = AssignmentTrackerApp(file_path)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()