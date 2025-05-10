from app import app, db
from models import SiteSettings

with app.app_context():
    settings = SiteSettings.query.first()
    print(f"Profile image path: {settings.profile_image}")
