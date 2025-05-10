from app import app, db
from models import User, Project, Skill, Experience, Education, Certification, SiteSettings
from werkzeug.security import generate_password_hash
from datetime import date

def init_db():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        print("Creating admin user...")
        # Create admin user
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),  # Change this in production
            email='shamimjonym@gmail.com'
        )
        db.session.add(admin)
        
        print("Creating site settings...")
        # Create site settings
        settings = SiteSettings(
            site_title="Shamim MD Jony - Portfolio",
            hero_title="Shamim MD Jony",
            hero_subtitle="Machine Learning Engineer",
            about_text="Experienced machine learning enthusiast with expertise in developing and deploying machine learning models and large language models (LLMs). Proficient in deep learning, computer vision, and NLP, with a focus on building scalable AI solutions. Skilled in optimizing algorithms and integrating advanced technologies into real-world applications.",
            profile_image="/static/images/profile.png",
            github_url="https://github.com/shamimjony1000",
            linkedin_url="https://www.linkedin.com/in/shamimjony-9b38662a0",
            email="shamimjonym@gmail.com",
            phone="+8801816435862",
            location="Khulshi-1, Chittagong, Bangladesh"
        )
        db.session.add(settings)
        
        print("Adding skills...")
        # Add skills
        skills = [
            Skill(name="Large Language Models (LLMs)", category="ml_ai"),
            Skill(name="LLMs Fine-Tuning", category="ml_ai"),
            Skill(name="Computer Vision", category="ml_ai"),
            Skill(name="Natural Language Processing", category="ml_ai"),
            Skill(name="Deep Learning", category="ml_ai"),
            Skill(name="Python", category="programming"),
            Skill(name="C/C++", category="programming"),
            Skill(name="Java", category="programming"),
            Skill(name="PHP", category="programming"),
            Skill(name="HTML/CSS/JavaScript", category="programming"),
            Skill(name="Flask", category="programming"),
            Skill(name="FastAPI", category="programming"),
            Skill(name="PHP Laravel", category="programming"),
            Skill(name="MySQL", category="programming"),
            Skill(name="SQLite", category="programming"),
            Skill(name="MongoDB", category="programming"),
            Skill(name="AWS Lightsail", category="deployment"),
            Skill(name="AWS", category="deployment"),
            Skill(name="Google Cloud", category="deployment"),
            Skill(name="API Development", category="deployment"),
        ]
        for skill in skills:
            db.session.add(skill)
        
        print("Adding projects...")
        # Add projects
        projects = [
            Project(
                title="Smart FAQ Chatbot",
                category="llm",
                description="Revolutionizing E-Commerce with Intelligent Shopping Assistance. This project leverages LangChain to create a context-aware chatbot that can answer customer questions about products, shipping, and returns.",
                technologies="LangChain, Python, LLMs, Vector Database, NLP",
                featured=True
            ),
            Project(
                title="Clinical Text Classification",
                category="ml",
                description="BSc Thesis project focused on medical text classification using advanced deep learning techniques. Developed approaches for classifying clinical text data to improve medical document categorization to assist healthcare professionals in quickly identifying relevant patient information.",
                technologies="Deep Learning, NLP, Python, TensorFlow, BERT",
                featured=True
            ),
            Project(
                title="Bangladeshi Airline Sentiment Classification",
                category="ml",
                description="Analyzed customer reviews and feedback for Bangladeshi airlines using both traditional machine learning and deep learning techniques to classify sentiment and identify areas for service improvement.",
                technologies="Sentiment Analysis, Machine Learning, Deep Learning, Python, NLP",
                featured=False
            ),
            Project(
                title="Bangla Hate Speech Detection",
                category="ml",
                description="Created models to detect and classify hate speech in Bangla text using both machine learning and deep learning approaches. This project addresses the challenge of content moderation in Bangla language social media.",
                technologies="NLP, Machine Learning, Deep Learning, Python, Text Classification",
                featured=False
            ),
            Project(
                title="E-commerce Platform Development",
                category="other",
                description="Contributed to the development and scaling of e-commerce solutions at Prachine Bangla Ecommerce Limited, focusing on high traffic support and large product catalogs.",
                technologies="AWS Lightsail, API Development, PHP, Laravel, MySQL",
                featured=False
            ),
        ]
        for project in projects:
            db.session.add(project)
        
        print("Adding experience...")
        # Add experience
        experience = Experience(
            title="Software Engineer",
            company="Prachine Bangla Ecommerce Limited",
            start_date=date(2024, 11, 1),  # November 2024
            end_date=None,  # Current position
            description="Managing the main AWS Lightsail server infrastructure. Developing and scaling e-commerce solutions to support high traffic and large product catalogs. Integrating AI-powered chatbots to improve customer support and engagement. Collaborating on API development and third-party service integrations (payment gateways, shipping, etc.)."
        )
        db.session.add(experience)
        
        print("Adding education...")
        # Add education
        educations = [
            Education(
                degree="Bachelor of Science in CSE (BSc)",
                institution="Port City International University",
                year=2023,
                gpa="3.88 out of 4"
            ),
            Education(
                degree="Diploma in Computer Science & Engineering",
                institution="Landmark Polytechnic Institute",
                year=2017,
                gpa="3.59 out of 4"
            )
        ]
        for education in educations:
            db.session.add(education)
        
        print("Adding certifications...")
        # Add certifications
        certifications = [
            Certification(
                name="LangChain Chat with Your Data!",
                issuer="deeplearning.ai",
                year=2024
            ),
            Certification(
                name="ChatGPT Prompt Engineering for Developers",
                issuer="deeplearning.ai",
                year=2024
            )
        ]
        for certification in certifications:
            db.session.add(certification)
            
        print("Committing changes to database...")
        db.session.commit()
        print("Database initialization complete!")

if __name__ == "__main__":
    init_db()
