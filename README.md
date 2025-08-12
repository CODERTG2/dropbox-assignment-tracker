# Assignment Tracker

A secure desktop application for tracking assignments using Google Sheets integration.

## 🔒 Security Features

- **No embedded credentials**: Your API keys and credentials are never distributed with the app
- **Local storage**: Credentials are stored securely on your local machine only
- **User-controlled access**: You provide your own Google Sheets credentials
- **Setup wizard**: Easy first-time configuration with validation

## 📋 Prerequisites

Before installing, make sure you have:

1. **Python 3.7 or higher** installed on your system
2. **Google Sheets API credentials** (we'll help you get these)
3. **A Google Sheet** set up for tracking assignments

## 🚀 Quick Start

### Option 1: Mac Installer (Recommended for macOS)

Download and run the Mac installer: `AssignmentTracker-Installer.dmg`

1. Download the DMG file from the [releases](../../releases) section
2. Open the DMG file
3. Drag the Assignment Tracker app to your Applications folder
4. Launch the app from Applications

**Windows installer coming soon!**

### Option 2: Script Installation

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Option 3: Manual Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python3 main.py
   ```

## 🔧 First-Time Setup

When you first run the application, you'll see a setup wizard that guides you through:

1. **Getting Google Sheets API credentials**
2. **Entering your credentials securely**
3. **Configuring your Google Sheets ID**
4. **Testing the connection**

### Getting Google Sheets API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API
4. Create credentials (Service Account)
5. Download the JSON key file
6. Share your Google Sheet with the service account email

**The setup wizard provides detailed step-by-step instructions with links!**

## 💻 Usage

### Basic Usage
```bash
python3 main.py
```

### With a specific file
```bash
python3 main.py "/path/to/your/document.docx"
```

### Features

- **Assignment Management**: Create, edit, and track assignments
- **Google Sheets Integration**: Automatic sync with your spreadsheet
- **File Association**: Link assignments to specific documents
- **Progress Tracking**: Not Started, In Progress, Completed
- **Due Date Management**: Set and track deadlines
- **Assignee Tracking**: Assign work to team members

## 🛠️ Configuration

### Credentials Location
Your credentials are stored in:
- **macOS/Linux**: `~/.assignment_tracker/`
- **Windows**: `%USERPROFILE%\.assignment_tracker\`

### Files Created
- `credentials.json`: Your Google Sheets API credentials
- `.env`: Your configuration (Sheet ID, etc.)

### Reconfiguring
Click the "Settings" button in the app to reconfigure your credentials anytime.

## 🔒 Security Best Practices

### What We Do
- Store credentials locally only
- Never transmit credentials to external servers
- Validate credentials before saving
- Provide secure setup wizard
- Use encrypted connection to Google Sheets

### What You Should Do
- Keep your credentials file secure
- Don't share your service account JSON file
- Regularly rotate your API keys
- Only share your Google Sheet with necessary accounts
- Use the principle of least privilege

## 🏗️ Building Executables

### For Distribution

**macOS:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "setup_wizard.py:." main.py
```

**Windows:**
```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "setup_wizard.py;." main.py
```

**Linux:**
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "setup_wizard.py:." main.py
```

## 📁 Project Structure

```
assignment-tracker/
├── main.py                           # Main application
├── setup_wizard.py                   # Secure credential setup
├── SheetReader.py                    # Google Sheets integration
├── requirements.txt                  # Python dependencies
├── install.sh                       # macOS/Linux installer script
├── install.bat                      # Windows installer script
├── installers/
│   └── AssignmentTracker-Installer.dmg  # Mac installer package
└── README.md                        # This file
```

## ⚠️ Important Security Notes

- **Never commit credentials to version control**
- **Never distribute apps with embedded API keys**
- **Always use the setup wizard for credential management**
- **Regularly audit who has access to your Google Sheets**

## 🆘 Troubleshooting

### Common Issues

**"No module named 'PyQt5'"**
```bash
pip3 install PyQt5
```

**"Could not connect to Google Sheets"**
- Check your credentials are valid
- Verify your Sheet ID is correct
- Ensure the sheet is shared with your service account

**"Permission denied" errors**
- Make sure your service account has edit access to the sheet
- Check that the Google Sheets API is enabled

### Getting Help

1. Check the built-in help in the setup wizard
2. Review the step-by-step credential guide
3. Verify your Google Cloud Console settings
4. Test your connection using the built-in test feature

---

**Built with security and user privacy in mind**
