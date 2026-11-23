from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()

admin = Admin()


class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    # Relationship: One band has many members + albums
    # members = db.relationship('Members', backref='band', lazy=True)
    # albums = db.relationship('Albums', backref='band', lazy=True)
    memberships = db.relationship("Memberships",backref="band",lazy=True)
    albumships = db.relationship("Albumships",backref="band",lazy=True)


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    # BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    memberships = db.relationship("Memberships",backref='member',lazy=True)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))


class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
    albumships = db.relationship("Albumships",backref="album",lazy=True)

class Memberships(db.Model):
    MembershipID = db.Column(db.Integer,primary_key=True)
    BandID = db.Column(db.Integer,db.ForeignKey("bands.BandID"),nullable=False)
    MemberID = db.Column(db.Integer,db.ForeignKey('members.MemberID'),nullable=False)
    Role = db.Column(db.String(80))
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)

class Albumships(db.Model):
    AlbumshipID = db.Column(db.Integer,primary_key=True)
    BandID = db.Column(db.Integer,db.ForeignKey("bands.BandID"),nullable=False)
    AlbumID = db.Column(db.Integer,db.ForeignKey('albums.AlbumID'),nullable=False)
    Title = db.Column(db.String(80))
    Release = db.Column(db.Integer)