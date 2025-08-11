from SheetReader import SheetReader
from DropboxClient import DropboxClient
from dotenv import load_dotenv
import os
import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QPushButton, QTextEdit, QComboBox, 
                           QLineEdit, QRadioButton, QButtonGroup, QFrame, 
                           QScrollArea, QMessageBox, QProgressBar, QSizePolicy)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QColor

load_dotenv()

class LoadAssignmentsThread(QThread):
    """Thread for loading assignments to prevent UI blocking"""
    finished = Signal(list)
    error = Signal(str)
    
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
        self.setup_ui()
        self.setup_clients()
        self.apply_modern_styling()
        
        if file_path:
            self.process_file(file_path)
    
    def setup_ui(self):
        self.setWindowTitle("Assignment Tracker - Modern Interface")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QVBoxLayout()
        
        title_label = QLabel("📋 Assignment Tracker")
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        
        if self.file_path:
            self.file_label = QLabel(f"📁 Current File: {os.path.basename(self.file_path)}")
            self.file_label.setObjectName("subtitle")
            header_layout.addWidget(self.file_label)
        
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)
        
        # Assignment selection section
        selection_frame = QFrame()
        selection_frame.setFrameStyle(QFrame.StyledPanel)
        selection_layout = QVBoxLayout()
        
        selection_title = QLabel("🔍 Select Assignment")
        selection_title.setObjectName("section_title")
        selection_layout.addWidget(selection_title)
        
        # Dropdown and search layout
        dropdown_layout = QHBoxLayout()
        self.assignment_dropdown = QComboBox()
        self.assignment_dropdown.setEditable(True)
        self.assignment_dropdown.setPlaceholderText("Search or select an assignment...")
        self.assignment_dropdown.currentTextChanged.connect(self.on_assignment_changed)
        
        self.search_button = QPushButton("🔍 Load Assignment")
        self.search_button.clicked.connect(self.load_assignment_details)
        self.search_button.setEnabled(False)
        
        dropdown_layout.addWidget(self.assignment_dropdown, 3)
        dropdown_layout.addWidget(self.search_button, 1)
        selection_layout.addLayout(dropdown_layout)
        
        # Loading indicator
        self.loading_bar = QProgressBar()
        self.loading_bar.setVisible(False)
        selection_layout.addWidget(self.loading_bar)
        
        selection_frame.setLayout(selection_layout)
        main_layout.addWidget(selection_frame)
        
        # Assignment details section (initially hidden)
        self.details_frame = QFrame()
        self.details_frame.setFrameStyle(QFrame.StyledPanel)
        self.details_frame.setVisible(False)
        self.setup_details_section()
        main_layout.addWidget(self.details_frame)
        
        # Status section
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("Status updates will appear here...")
        main_layout.addWidget(self.status_text)
        
        central_widget.setLayout(main_layout)
    
    def setup_details_section(self):
        details_layout = QVBoxLayout()
        
        details_title = QLabel("📝 Assignment Details")
        details_title.setObjectName("section_title")
        details_layout.addWidget(details_title)
        
        # Create a scroll area for the form
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        form_layout = QVBoxLayout()
        
        # Description field
        desc_label = QLabel("📄 Description:")
        desc_label.setObjectName("field_label")
        form_layout.addWidget(desc_label)
        self.description_field = QTextEdit()
        self.description_field.setMaximumHeight(100)
        self.description_field.setPlaceholderText("Enter assignment description...")
        form_layout.addWidget(self.description_field)
        
        # Due date field
        date_label = QLabel("📅 Due Date:")
        date_label.setObjectName("field_label")
        form_layout.addWidget(date_label)
        self.due_date_field = QLineEdit()
        self.due_date_field.setPlaceholderText("YYYY-MM-DD or any date format...")
        form_layout.addWidget(self.due_date_field)
        
        # Progress radio buttons
        progress_label = QLabel("⚡ Progress:")
        progress_label.setObjectName("field_label")
        form_layout.addWidget(progress_label)
        
        progress_layout = QHBoxLayout()
        self.progress_group = QButtonGroup()
        
        self.not_started_radio = QRadioButton("🚫 Not Started")
        self.wip_radio = QRadioButton("🔄 Work in Progress")
        self.done_radio = QRadioButton("✅ Done")
        
        self.progress_group.addButton(self.not_started_radio, 0)
        self.progress_group.addButton(self.wip_radio, 1)
        self.progress_group.addButton(self.done_radio, 2)
        
        progress_layout.addWidget(self.not_started_radio)
        progress_layout.addWidget(self.wip_radio)
        progress_layout.addWidget(self.done_radio)
        progress_layout.addStretch()
        
        form_layout.addLayout(progress_layout)
        
        # Assignee field
        assignee_label = QLabel("👤 Assignee:")
        assignee_label.setObjectName("field_label")
        form_layout.addWidget(assignee_label)
        self.assignee_field = QLineEdit()
        self.assignee_field.setPlaceholderText("Enter assignee name...")
        form_layout.addWidget(self.assignee_field)
        
        # Save button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.save_button = QPushButton("💾 Save Assignment")
        self.save_button.clicked.connect(self.save_assignment)
        self.save_button.setObjectName("save_button")
        button_layout.addWidget(self.save_button)
        form_layout.addLayout(button_layout)
        
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        details_layout.addWidget(scroll_area)
        
        self.details_frame.setLayout(details_layout)
    
    def apply_modern_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin: 5px;
            }
            
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            
            QLabel#subtitle {
                font-size: 14px;
                color: #7f8c8d;
                padding: 5px 10px;
            }
            
            QLabel#section_title {
                font-size: 18px;
                font-weight: bold;
                color: #34495e;
                margin-bottom: 10px;
            }
            
            QLabel#field_label {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            QComboBox {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            
            QComboBox:focus {
                border-color: #3498db;
            }
            
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                background-color: #3498db;
                color: white;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #21618c;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            
            QPushButton#save_button {
                background-color: #27ae60;
                padding: 12px 30px;
                font-size: 16px;
            }
            
            QPushButton#save_button:hover {
                background-color: #229954;
            }
            
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
            }
            
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
                padding: 10px;
            }
            
            QTextEdit:focus {
                border-color: #3498db;
            }
            
            QRadioButton {
                font-size: 14px;
                color: #2c3e50;
                spacing: 10px;
                margin-right: 20px;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            
            QRadioButton::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 9px;
                background-color: white;
            }
            
            QRadioButton::indicator:checked {
                border: 2px solid #3498db;
                border-radius: 9px;
                background-color: #3498db;
            }
            
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
            }
            
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
    
    def setup_clients(self):
        try:
            self.status_text.append("🔧 Initializing clients...")
            self.dropbox_client = DropboxClient(os.getenv("DROPBOXKEY"), "Northside Debate 2025-2026")
            self.sheet_reader = SheetReader("credentials.json", os.getenv("SHEET_ID"))
            self.status_text.append("✅ Clients initialized successfully")
            self.load_assignments()
        except Exception as e:
            self.status_text.append(f"❌ Error initializing clients: {str(e)}")
    
    def load_assignments(self):
        """Load assignments in a separate thread"""
        self.loading_bar.setVisible(True)
        self.loading_bar.setRange(0, 0)  # Indeterminate progress
        self.status_text.append("📊 Loading assignments from spreadsheet...")
        
        self.assignment_thread = LoadAssignmentsThread(self.sheet_reader)
        self.assignment_thread.finished.connect(self.on_assignments_loaded)
        self.assignment_thread.error.connect(self.on_assignments_error)
        self.assignment_thread.start()
    
    def on_assignments_loaded(self, assignments):
        """Handle successful assignment loading"""
        self.loading_bar.setVisible(False)
        self.assignment_dropdown.clear()
        self.assignment_dropdown.addItems(assignments)
        self.status_text.append(f"✅ Loaded {len(assignments)} assignments")
        self.search_button.setEnabled(True)
    
    def on_assignments_error(self, error_msg):
        """Handle assignment loading error"""
        self.loading_bar.setVisible(False)
        self.status_text.append(f"❌ Error loading assignments: {error_msg}")
        QMessageBox.critical(self, "Error", f"Failed to load assignments:\n{error_msg}")
    
    def on_assignment_changed(self):
        """Handle assignment dropdown change"""
        current_text = self.assignment_dropdown.currentText().strip()
        self.search_button.setEnabled(bool(current_text))
    
    def load_assignment_details(self):
        """Load details for the selected assignment"""
        assignment = self.assignment_dropdown.currentText().strip()
        if not assignment:
            return
        
        self.current_assignment = assignment
        self.status_text.append(f"📋 Loading details for: {assignment}")
        
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
            
            # Show details section
            self.details_frame.setVisible(True)
            self.status_text.append(f"✅ Loaded details for {assignment}")
            
        except Exception as e:
            self.status_text.append(f"❌ Error loading assignment details: {str(e)}")
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
            
            # Get file name and find in Dropbox
            file_name = os.path.basename(self.file_path)
            dropbox_path = self.dropbox_client.find_file_path(file_name)
            
            if not dropbox_path:
                self.status_text.append(f"⚠️ File {file_name} not found in Dropbox")
                dropbox_path = f"/path/to/{file_name}"  # Fallback path
            
            self.status_text.append(f"💾 Saving assignment: {self.current_assignment}")
            
            # Update spreadsheet
            self.sheet_reader.update_record(
                assignment=self.current_assignment,
                file_path=dropbox_path,
                description=description,
                due_date=due_date,
                progress=progress,
                assignee=assignee
            )
            
            # Update or add Dropbox metadata
            metadata = {
                "assignment_name": self.current_assignment,
                "description": description,
                "due_date": due_date,
                "progress": progress,
                "assignee": assignee
            }
            
            if self.is_updating:
                # Update existing metadata
                for key, value in metadata.items():
                    self.dropbox_client.update_metadata(file_name, key, value)
                self.status_text.append(f"🔄 Updated metadata for {file_name}")
            else:
                # Add new metadata
                self.dropbox_client.add_metadata(file_name, metadata)
                self.status_text.append(f"➕ Added metadata for {file_name}")
            
            self.status_text.append(f"✅ Successfully saved assignment: {self.current_assignment}")
            QMessageBox.information(self, "Success", f"Assignment '{self.current_assignment}' saved successfully!")
            
        except Exception as e:
            error_msg = f"Failed to save assignment: {str(e)}"
            self.status_text.append(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def process_file(self, file_path):
        # Extract filename and clean the path to exclude everything from "dropbox" and before
        file_name = os.path.basename(file_path)
        
        # If the path contains "dropbox", extract everything after it
        if "dropbox" in file_path.lower():
            # Find the position of "dropbox" (case insensitive)
            dropbox_index = file_path.lower().find("dropbox")
            # Extract the path from after "dropbox/"
            cleaned_path = file_path[dropbox_index:]
            # Remove "dropbox/" or "dropbox\" from the beginning
            if cleaned_path.lower().startswith("dropbox/") or cleaned_path.lower().startswith("dropbox\\"):
                cleaned_path = cleaned_path[8:]  # Remove "dropbox/" or "dropbox\"
            self.status_text.append(f"📁 Processing file: {file_name}")
            self.status_text.append(f"📂 Cleaned path: {cleaned_path}")
        else:
            # If no "dropbox" in path, just use the filename
            self.status_text.append(f"📁 Processing file: {file_name}")
            self.status_text.append(f"📂 Original path: {file_path}")
        
        # Check if file exists in Dropbox
        try:
            dropbox_path = self.dropbox_client.find_file_path(file_name)
            if dropbox_path:
                self.status_text.append(f"☁️ Found in Dropbox: {dropbox_path}")
            else:
                self.status_text.append("⚠️ File not found in Dropbox folder")
        except Exception as e:
            self.status_text.append(f"❌ Error checking Dropbox: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # Set application properties for better styling
    app.setStyle('Fusion')
    
    # Get file path from command line arguments
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Opened with file: {file_path}")
        # Extract just the filename for display
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")
    else:
        print("No file specified via command line")
    
    window = AssignmentTrackerApp(file_path)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()