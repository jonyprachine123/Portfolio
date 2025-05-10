# Shamim MD Jony - Portfolio Website

A Flask-based portfolio website showcasing my skills, projects, and experience as a Machine Learning Engineer.

## Features

- Responsive design using Bootstrap 5
- Interactive UI with custom animations
- Sections for projects, resume, and contact information
- Contact form for potential clients or employers to reach out

## Project Structure

```
Portfolio/
├── app.py                 # Main Flask application file
├── requirements.txt       # Python dependencies
├── static/                # Static files
│   ├── css/               # CSS stylesheets
│   │   └── style.css      # Custom styles
│   ├── js/                # JavaScript files
│   │   └── main.js        # Custom scripts
│   └── images/            # Image assets
├── templates/             # HTML templates
│   ├── base.html          # Base template with common elements
│   ├── index.html         # Home page
│   ├── projects.html      # Projects showcase
│   ├── resume.html        # Resume/CV page
│   ├── contact.html       # Contact form
│   └── thank_you.html     # Form submission confirmation
└── README.md              # Project documentation
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Portfolio
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Customization

- **Profile Image**: Add your profile image to the `static/images/` directory and update the reference in `index.html`
- **Content**: Modify the HTML templates to update your personal information, projects, and skills
- **Styling**: Customize the appearance by editing `static/css/style.css`

## Deployment

This Flask application can be deployed to various platforms:

- **Heroku**: Create a `Procfile` with `web: gunicorn app:app`
- **PythonAnywhere**: Follow their Flask deployment guide
- **AWS**: Deploy using Elastic Beanstalk or EC2

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons
- **Animations**: Custom CSS animations

## Contact

- **Email**: shamimjonym@gmail.com
- **GitHub**: [github.com/shamimjony1000](https://github.com/shamimjony1000)
- **LinkedIn**: [linkedin.com/in/shamimjony-9b38662a0](https://www.linkedin.com/in/shamimjony-9b38662a0)
