from app import app, db
from models import SiteSettings

with app.app_context():
    settings = SiteSettings.query.first()
    print(f"Old profile image path: {settings.profile_image}")
    settings.profile_image = "/static/images/profile.png"
    db.session.commit()
    print(f"New profile image path: {settings.profile_image}")
    print("Profile image path updated successfully!")
