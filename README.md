# Resume Builder Web Application with AI Integration

## Project Overview

This project is a web-based application built with Django, designed to help students and job seekers automatically create and customize their resumes. The app allows users to enter data through forms, generate a PDF version of their resume, integrate projects from GitHub, upload certificates, and diplomas, and automatically send the resume to job portals. An integrated AI system helps to write cover letters, filter resume information, and provide personalized suggestions based on job requirements.

### Key Features

1. **Resume Creation:**
   - Form-based input for user data (work experience, education, skills, etc.).
   - Automatic PDF generation from templates.
   - Resume preview functionality.
   - Customizable resume templates with a drag-and-drop layout editor.

2. **GitHub Integration:**
   - Link to user’s GitHub profile.
   - Automatic extraction and addition of projects to the resume.

3. **Document Upload:**
   - Upload diplomas, certificates, and other supporting documents.

4. **Employer Interaction:**
   - Employers can view resumes, mark suitable candidates, and send approval emails.

5. **AI-Assisted Cover Letter Generation:**
   - AI generates personalized cover letters based on job requirements.
   - Information is filtered to match specific industries (e.g., construction, IT).

6. **AI-Powered Assistance:**
   - AI helps users fill out specific resume sections (e.g., work experience, skills).
   - Analyzes and optimizes the resume for specific job roles.
   - Provides suggestions on what to improve or remove from the resume.
   - Generates resume variations tailored for specific job applications.

7. **Integration with Job Portals:**
   - Automatic submission of resumes to job portals (e.g., LinkedIn, Indeed).
   - AI filters job vacancies and suggests the most relevant ones.

8. **AI Assistance for Employers:**
   - Employers can use AI to filter resumes based on job requirements and skills.
   - AI highlights the most suitable candidates.

### Technologies Used

- **Django**: Backend framework for form handling, user authentication, and database management.
- **PostgreSQL/MySQL**: Database for storing user data, resumes, and documents.
- **WeasyPrint/ReportLab**: Libraries for generating PDF resumes.
- **GitHub API**: To pull user projects for resume enhancement.
- **AI Integration**: For generating cover letters, filtering resume data, and providing suggestions.

## API Endpoints

- `POST /resumes`: Create a new resume.
- `GET /resumes/:id`: Retrieve details of a specific resume by ID.
- `PUT /resumes/:id`: Update an existing resume.
- `DELETE /resumes/:id`: Delete a resume.
- `POST /cover-letter`: AI-assisted cover letter generation.  
## Site Routes

Here is an overview of the main routes in the application:

1. **Home Page**: `/`
   - Main landing page with an overview of the features.

2. **Create a New Resume**: `/resumes/create/`
   - Form for creating a new resume with sections for education, experience, and skills.

3. **View Resumes**: `/resumes/`
   - List of all resumes created by the user, with options to edit, delete, or preview.

4. **View Specific Resume**: `/resumes/<id>/`
   - Detailed view of a resume by its ID. Includes an option to download as PDF.

5. **Edit Resume**: `/resumes/<id>/edit/`
   - Edit an existing resume's content and layout.

6. **Delete Resume**: `/resumes/<id>/delete/`
   - Confirmation page to delete a resume.

7. **GitHub Integration**:
   - **Connect GitHub**: `/account/github/connect/`
     - Connect a GitHub account to import projects.
   - **View GitHub Projects**: `/resumes/<id>/projects/`
     - View and select GitHub projects to include in the resume.

8. **Generate AI Cover Letter**: `/resumes/<id>/cover-letter/`
   - Use AI to generate a cover letter tailored to a specific job.

9. **AI Resume Optimization**: `/resumes/<id>/optimize/`
   - AI analyzes the resume and provides suggestions for improvement.

10. **Employer's Resume View**: `/employers/resumes/<id>/`
    - Employers can view a candidate's resume, provide feedback, and mark as approved.

11. **Upload Documents**: `/resumes/<id>/documents/upload/`
    - Upload certificates, diplomas, or other relevant documents.

12. **View Uploaded Documents**: `/resumes/<id>/documents/`
    - View or manage uploaded documents.

13. **Admin Panel**: `/admin/`
    - Standard Django admin interface for managing users, resumes, and documents.


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
