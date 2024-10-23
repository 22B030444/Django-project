## Team members

| Student name          | Student ID      |
|-----------------------|-----------------|
| Suleimenova Zhasmin   | 22B030444       |
| Tolegen Nursultan     | 22B030453       |
| Taubaev Azamat        | 22B030450       |
| Temirgali Rustem      | 22B030451       |
| Smanova Alua          | 22B031106       |

# Resume Builder Web Application with AI Integration

## Project Overview

The Resume Builder Web Application is designed to assist students in creating professional resumes automatically. Users can fill out a form, which generates a formatted PDF resume for download. The application also integrates with GitHub to fetch projects, allows users to upload diplomas and certificates, and provides features for employers to view resumes and send feedback. An AI component will help generate tailored cover letters based on the job requirements.

## Functional Requirements

### User Roles

1. **Users**
   - Can register and log in to the application.
   - Users can be classified as:
     - **Workers** (job seekers)
     - **Employers**

### Worker Features

1. **Resume Creation**
   - Fill out a user-friendly form to input personal details, education, work experience, and skills.
   - Select from various resume templates.
   - Use a resume constructor to organize and format information.
   - Preview the resume before downloading.

2. **GitHub Integration**
   - Connect to GitHub to fetch and display projects.
   - Include GitHub projects in the resume.

3. **Document Upload**
   - Upload diplomas and certificates to include in the resume.

4. **AI-Assisted Cover Letter Generation**
   - Access an embedded chatbot to help write cover letters tailored to specific job roles and companies.

5. **PDF Generation**
   - Generate a downloadable PDF version of the resume.

6. **Job Application Submission**
   - Send the created resume to job search websites.

### Employer Features

1. **Resume Viewing**
   - View resumes submitted by workers.
   - Mark resumes as suitable for further consideration.

2. **Feedback and Approval**
   - Send approval emails to workers regarding their resumes.

### General Features

1. **User Management**
   - Implement registration, login, and logout functionality.
   - Allow users to manage their profiles.

2. **Admin Dashboard**
   - Admins can view all users and manage resumes and applications.

3. **Responsive Design**
   - Ensure the application is mobile-friendly and accessible on various devices.

4. **Security**
   - Implement secure authentication and data handling practices.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (or any other preferred database)
- **AI Integration**: OpenAI API (for cover letter generation)
- **GitHub API**: For fetching user projects

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd resume-builder
   ```

3. Create a virtual environment:
   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or suggestions.

## License

This project is licensed under the MIT License.


## API Routes

### User Authentication
- **POST /register**: Register a new user.
- **POST /login**: Authenticate a user and return a token.
- **POST /logout**: Log out the authenticated user.

### Worker Features
- **POST /resumes**: Create a new resume.
- **GET /resumes**: Retrieve all resumes for the authenticated worker.
- **GET /resumes/{id}**: Retrieve a specific resume by ID.
- **PUT /resumes/{id}**: Update an existing resume.
- **DELETE /resumes/{id}**: Delete a specific resume.

### Document Upload
- **POST /resumes/{id}/documents**: Upload diplomas or certificates associated with a specific resume.

### GitHub Integration
- **GET /github/projects**: Fetch projects from the authenticated user's GitHub account.

### AI Assistance
- **POST /cover-letter**: Generate a cover letter based on the specified job requirements.

### Employer Features
- **GET /employers/resumes**: Retrieve all resumes submitted by workers for employers.
- **POST /employers/resumes/{id}/feedback**: Send feedback or approval for a specific resume.

## AI Features

- **Content Filtering**: AI helps structure and filter resume content for different job types and industries.
- **Custom Cover Letters**: AI generates tailored cover letters based on job requirements.
- **Resume Optimization**: AI offers suggestions for improving resume structure and content.

#### Prerequisites

- Python 3.x
- Django 3.x or later
- PostgreSQL or MySQL
- GitHub account for API integration

#### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resume-builder.git

## Contribution

We welcome contributions! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.
