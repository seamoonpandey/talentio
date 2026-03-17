
# Quick CV

Quick CV is a modern web-based application for building, previewing, and exporting professional CVs with ease. Users can create, edit, and manage their CVs, then export them as PDFs for job applications or personal use.

## Features

- Intuitive drag-and-drop CV editor
- Multiple professional templates
- Real-time preview
- PDF export functionality
- User authentication and profile management
- Responsive design for desktop and mobile

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** MongoDB Atlas
- **PDF Export:** jsPDF

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for frontend development, optional)
- MongoDB Atlas account (or local MongoDB)

### Installation

1. **Clone the repository:**

 ```bash
 git clone https://github.com/seamoonpandey/quickcv.git
 cd quick-cv
 ```

1. **Set up the backend:**

 ```bash
 cd backend
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate
 pip install -r requirements.txt
 cp .env.example .env      # Create your .env file with the required variables
 python run.py
 ```

1. **Open the frontend:**

- Open `frontend/index.html` in your browser
- Or use VS Code Live Server for local development

## Project Structure

```bash
quick-cv/
├── backend/    # Flask REST API and business logic
├── frontend/   # HTML, CSS, JS (UI layer)
├── deploy/     # Deployment scripts and configs
├── docs/       # Documentation and wireframes
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
