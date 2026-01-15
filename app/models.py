from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50)) # e.g., 'Cafe', 'Club', 'Culture'
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # --- PROFESSOR'S KEY REQUIREMENTS ---
    cultural_etiquette = db.Column(db.Text) # Tips for tourists
    
    # --- UI ENHANCEMENT ---
    # Adding a default image so your dashboard looks professional
    image_url = db.Column(db.String(255), default="https://images.unsplash.com/photo-1580674239581-3fbc1917a167?q=80&w=1000&auto=format&fit=crop")

    def to_dict(self):
        """Helper to convert database objects to JSON for your API"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "cultural_etiquette": self.cultural_etiquette,
            "image_url": self.image_url
        }