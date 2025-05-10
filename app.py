from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
import os
import uuid
from models import db, User, Project, Skill, Experience, Education, Certification, ContactMessage, SiteSettings, Visitor
from forms import (LoginForm, ProjectForm, SkillForm, ExperienceForm, EducationForm, 
                  CertificationForm, SiteSettingsForm, ChangePasswordForm)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads/projects')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add unique identifier to prevent filename collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return f"/static/uploads/projects/{unique_filename}"
    return None

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    
# Track page visits
@app.before_request
def track_visitor():
    # Only track GET requests to public pages
    if request.method == 'GET' and not request.path.startswith('/dashboard') and not request.path.startswith('/admin') and not request.path.startswith('/static'):
        try:
            visitor = Visitor(
                page=request.path,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string if request.user_agent else None,
                referrer=request.referrer
            )
            db.session.add(visitor)
            db.session.commit()
        except Exception as e:
            # Log the error but don't interrupt the user's request
            print(f"Error tracking visitor: {e}")
            db.session.rollback()

# Public routes
@app.route('/')
def index():
    settings = SiteSettings.query.first()
    featured_projects = Project.query.filter_by(featured=True).all()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    educations = Education.query.order_by(Education.year.desc()).all()
    certifications = Certification.query.all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render_template('index.html', 
                          settings=settings,
                          featured_projects=featured_projects,
                          skills_by_category=skills_by_category,
                          experiences=experiences,
                          educations=educations,
                          certifications=certifications)

@app.route('/projects')
def projects():
    # Get all projects and categorize them
    llm_projects = Project.query.filter_by(category='llm').all()
    ml_projects = Project.query.filter_by(category='ml').all()
    other_projects = Project.query.filter(Project.category.notin_(['llm', 'ml'])).all()
    
    settings = SiteSettings.query.first()
    
    return render_template('projects.html', 
                           llm_projects=llm_projects, 
                           ml_projects=ml_projects, 
                           other_projects=other_projects,
                           settings=settings)

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
    # Get the project
    project = Project.query.get_or_404(project_id)
    
    # Get related projects (same category, excluding current)
    related_projects = Project.query.filter_by(category=project.category).filter(Project.id != project.id).limit(5).all()
    
    # If we don't have enough related projects, get some from other categories
    if len(related_projects) < 5:
        more_projects = Project.query.filter(Project.id != project.id).filter(Project.category != project.category).limit(5 - len(related_projects)).all()
        related_projects.extend(more_projects)
    
    settings = SiteSettings.query.first()
    
    return render_template('project_detail.html',
                           project=project,
                           related_projects=related_projects,
                           settings=settings)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = SiteSettings.query.first()
    if request.method == 'POST':
        # Save the contact message to the database
        message = ContactMessage(
            name=request.form.get('name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message')
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('contact.html', settings=settings)

@app.route('/thank-you')
def thank_you():
    settings = SiteSettings.query.first()
    return render_template('thank_you.html', settings=settings)

@app.route('/resume')
def resume():
    settings = SiteSettings.query.first()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    educations = Education.query.order_by(Education.year.desc()).all()
    certifications = Certification.query.all()
    skills = Skill.query.all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render_template('resume.html', 
                          settings=settings,
                          experiences=experiences,
                          educations=educations,
                          certifications=certifications,
                          skills_by_category=skills_by_category)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('admin/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard routes
@app.route('/dashboard')
@login_required
def dashboard():
    # Get counts for dashboard
    project_count = Project.query.count()
    skill_count = Skill.query.count()
    experience_count = Experience.query.count()
    education_count = Education.query.count()
    certification_count = Certification.query.count()
    message_count = ContactMessage.query.count()
    unread_message_count = ContactMessage.query.filter_by(read=False).count()
    
    # Get recent messages for quick view
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    # Get recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    
    # Get visitor analytics
    from sqlalchemy import func
    today = datetime.now().date()
    
    # Total visitors
    total_visitors = Visitor.query.count()
    
    # Today's visitors
    today_visitors = Visitor.query.filter(Visitor.visit_date == today).count()
    
    # Visitors by page
    page_visits = db.session.query(
        Visitor.page, func.count(Visitor.id).label('count')
    ).group_by(Visitor.page).order_by(func.count(Visitor.id).desc()).limit(5).all()
    
    # Visitors by date (last 7 days)
    from datetime import timedelta
    last_week = today - timedelta(days=7)
    visitors_by_date = db.session.query(
        Visitor.visit_date, func.count(Visitor.id).label('count')
    ).filter(Visitor.visit_date >= last_week)\
    .group_by(Visitor.visit_date)\
    .order_by(Visitor.visit_date.desc()).all()
    
    return render_template('admin/dashboard.html',
                          project_count=project_count,
                          skill_count=skill_count,
                          experience_count=experience_count,
                          education_count=education_count,
                          certification_count=certification_count,
                          message_count=message_count,
                          unread_message_count=unread_message_count,
                          recent_messages=recent_messages,
                          recent_projects=recent_projects,
                          total_visitors=total_visitors,
                          today_visitors=today_visitors,
                          page_visits=page_visits,
                          visitors_by_date=visitors_by_date)

# Project management
@app.route('/dashboard/projects')
@login_required
def manage_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects/index.html', projects=projects)

@app.route('/dashboard/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        # Handle image upload
        image_url = form.image_url.data
        if form.image_upload.data:
            uploaded_image_url = save_uploaded_file(form.image_upload.data)
            if uploaded_image_url:
                image_url = uploaded_image_url
        
        project = Project(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            technologies=form.technologies.data,
            image_url=image_url,
            project_url=form.project_url.data,
            github_url=form.github_url.data,
            youtube_url=form.youtube_url.data,
            featured=form.featured.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('manage_projects'))
    
    return render_template('admin/projects/create.html', form=form)

@app.route('/dashboard/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        # Handle image upload
        if form.image_upload.data:
            uploaded_image_url = save_uploaded_file(form.image_upload.data)
            if uploaded_image_url:
                project.image_url = uploaded_image_url
        elif form.image_url.data != project.image_url:
            # Only update image_url if it's changed and no file was uploaded
            project.image_url = form.image_url.data
            
        project.title = form.title.data
        project.category = form.category.data
        project.description = form.description.data
        project.technologies = form.technologies.data
        project.project_url = form.project_url.data
        project.github_url = form.github_url.data
        project.youtube_url = form.youtube_url.data
        project.featured = form.featured.data
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('manage_projects'))
    
    return render_template('admin/projects/edit.html', form=form, project=project)

@app.route('/dashboard/projects/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('manage_projects'))

# Skills management
@app.route('/dashboard/skills')
@login_required
def manage_skills():
    skills = Skill.query.all()
    return render_template('admin/skills/index.html', skills=skills)

@app.route('/dashboard/skills/create', methods=['GET', 'POST'])
@login_required
def create_skill():
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data,
            category=form.category.data
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill created successfully!', 'success')
        return redirect(url_for('manage_skills'))
    
    return render_template('admin/skills/create.html', form=form)

@app.route('/dashboard/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    form = SkillForm(obj=skill)
    
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('manage_skills'))
    
    return render_template('admin/skills/edit.html', form=form, skill=skill)

@app.route('/dashboard/skills/delete/<int:id>', methods=['POST'])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('manage_skills'))

# Experience management
@app.route('/dashboard/experiences')
@login_required
def manage_experiences():
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template('admin/experiences/index.html', experiences=experiences)

@app.route('/dashboard/experiences/create', methods=['GET', 'POST'])
@login_required
def create_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        experience = Experience(
            title=form.title.data,
            company=form.company.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data
        )
        db.session.add(experience)
        db.session.commit()
        flash('Experience created successfully!', 'success')
        return redirect(url_for('manage_experiences'))
    
    return render_template('admin/experiences/create.html', form=form)

@app.route('/dashboard/experiences/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    form = ExperienceForm(obj=experience)
    
    if form.validate_on_submit():
        experience.title = form.title.data
        experience.company = form.company.data
        experience.start_date = form.start_date.data
        experience.end_date = form.end_date.data
        experience.description = form.description.data
        experience.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('manage_experiences'))
    
    return render_template('admin/experiences/edit.html', form=form, experience=experience)

@app.route('/dashboard/experiences/delete/<int:id>', methods=['POST'])
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('manage_experiences'))

# Education management
@app.route('/dashboard/educations')
@login_required
def manage_educations():
    educations = Education.query.order_by(Education.year.desc()).all()
    return render_template('admin/educations/index.html', educations=educations)

@app.route('/dashboard/educations/create', methods=['GET', 'POST'])
@login_required
def create_education():
    form = EducationForm()
    if form.validate_on_submit():
        education = Education(
            degree=form.degree.data,
            institution=form.institution.data,
            year=form.year.data,
            gpa=form.gpa.data
        )
        db.session.add(education)
        db.session.commit()
        flash('Education created successfully!', 'success')
        return redirect(url_for('manage_educations'))
    
    return render_template('admin/educations/create.html', form=form)

@app.route('/dashboard/educations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)
    form = EducationForm(obj=education)
    
    if form.validate_on_submit():
        education.degree = form.degree.data
        education.institution = form.institution.data
        education.year = form.year.data
        education.gpa = form.gpa.data
        
        db.session.commit()
        flash('Education updated successfully!', 'success')
        return redirect(url_for('manage_educations'))
    
    return render_template('admin/educations/edit.html', form=form, education=education)

@app.route('/dashboard/educations/delete/<int:id>', methods=['POST'])
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    flash('Education deleted successfully!', 'success')
    return redirect(url_for('manage_educations'))

# Certification management
@app.route('/dashboard/certifications')
@login_required
def manage_certifications():
    certifications = Certification.query.all()
    return render_template('admin/certifications/index.html', certifications=certifications)

@app.route('/dashboard/certifications/create', methods=['GET', 'POST'])
@login_required
def create_certification():
    form = CertificationForm()
    if form.validate_on_submit():
        certification = Certification(
            name=form.name.data,
            issuer=form.issuer.data,
            year=form.year.data,
            url=form.url.data
        )
        db.session.add(certification)
        db.session.commit()
        flash('Certification created successfully!', 'success')
        return redirect(url_for('manage_certifications'))
    
    return render_template('admin/certifications/create.html', form=form)

@app.route('/dashboard/certifications/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_certification(id):
    certification = Certification.query.get_or_404(id)
    form = CertificationForm(obj=certification)
    
    if form.validate_on_submit():
        certification.name = form.name.data
        certification.issuer = form.issuer.data
        certification.year = form.year.data
        certification.url = form.url.data
        
        db.session.commit()
        flash('Certification updated successfully!', 'success')
        return redirect(url_for('manage_certifications'))
    
    return render_template('admin/certifications/edit.html', form=form, certification=certification)

@app.route('/dashboard/certifications/delete/<int:id>', methods=['POST'])
@login_required
def delete_certification(id):
    certification = Certification.query.get_or_404(id)
    db.session.delete(certification)
    db.session.commit()
    flash('Certification deleted successfully!', 'success')
    return redirect(url_for('manage_certifications'))

# Messages management
@app.route('/dashboard/messages')
@login_required
def manage_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages/index.html', messages=messages)

@app.route('/dashboard/messages/view/<int:id>')
@login_required
def view_message(id):
    message = ContactMessage.query.get_or_404(id)
    if not message.read:
        message.read = True
        db.session.commit()
    return render_template('admin/messages/view.html', message=message)

@app.route('/dashboard/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('manage_messages'))

# Site settings
@app.route('/dashboard/settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    settings = SiteSettings.query.first()
    form = SiteSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        settings.site_title = form.site_title.data
        settings.hero_title = form.hero_title.data
        settings.hero_subtitle = form.hero_subtitle.data
        settings.about_text = form.about_text.data
        settings.profile_image = form.profile_image.data
        
        # Handle resume file upload
        if form.resume_file_upload.data:
            resume_file = form.resume_file_upload.data
            if resume_file and allowed_file(resume_file.filename):
                # Create a unique filename for the resume
                filename = secure_filename(resume_file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads/resume', unique_filename)
                resume_file.save(file_path)
                settings.resume_file = f"/static/uploads/resume/{unique_filename}"
        elif form.resume_file.data != settings.resume_file:
            # Only update resume_file if it's changed and no file was uploaded
            settings.resume_file = form.resume_file.data
            
        settings.github_url = form.github_url.data
        settings.linkedin_url = form.linkedin_url.data
        settings.email = form.email.data
        settings.phone = form.phone.data
        settings.location = form.location.data
        settings.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('site_settings'))
    
    return render_template('admin/settings.html', form=form, settings=settings)

# Change password
@app.route('/dashboard/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        user = current_user
        if check_password_hash(user.password, form.current_password.data):
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template('admin/change_password.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
