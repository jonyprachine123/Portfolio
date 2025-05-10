from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, PasswordField, DateField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('llm', 'LLM Project'), 
        ('ml', 'Machine Learning Project'), 
        ('web', 'Web Development'), 
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    technologies = StringField('Technologies Used', validators=[DataRequired(), Length(max=255)])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    image_upload = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    project_url = StringField('Project URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    youtube_url = StringField('YouTube Video URL', validators=[Optional(), URL()])
    featured = BooleanField('Featured Project')

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('ml_ai', 'Machine Learning & AI'), 
        ('programming', 'Programming & Development'), 
        ('deployment', 'Deployment & Infrastructure')
    ], validators=[DataRequired()])

class ExperienceForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()])

class EducationForm(FlaskForm):
    degree = StringField('Degree', validators=[DataRequired(), Length(max=100)])
    institution = StringField('Institution', validators=[DataRequired(), Length(max=100)])
    year = IntegerField('Year', validators=[DataRequired()])
    gpa = StringField('GPA', validators=[Optional(), Length(max=20)])

class CertificationForm(FlaskForm):
    name = StringField('Certification Name', validators=[DataRequired(), Length(max=100)])
    issuer = StringField('Issuer', validators=[DataRequired(), Length(max=100)])
    year = IntegerField('Year', validators=[Optional()])
    url = StringField('URL', validators=[Optional(), URL()])

class SiteSettingsForm(FlaskForm):
    site_title = StringField('Site Title', validators=[DataRequired(), Length(max=100)])
    hero_title = StringField('Hero Title', validators=[DataRequired(), Length(max=100)])
    hero_subtitle = StringField('Hero Subtitle', validators=[DataRequired(), Length(max=200)])
    about_text = TextAreaField('About Text', validators=[DataRequired()])
    profile_image = StringField('Profile Image URL', validators=[Optional()])
    resume_file_upload = FileField('Upload Resume', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'PDF or Word documents only!')])
    resume_file = StringField('Resume File URL', validators=[Optional()])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
