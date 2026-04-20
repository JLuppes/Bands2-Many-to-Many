from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()

admin = Admin()

band_album = db.Table(
    'band_album',
    db.Column('band_id', db.Integer, db.ForeignKey('bands.BandID'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.AlbumID'), primary_key=True)
)



class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    # Removed members relationship in favor of memberships
    # members = db.relationship('Members', backref='band', lazy=True)
    memberships = db.relationship('Memberships', backref='band', lazy=True)
    albums = db.relationship(
    'Albums',
    secondary=band_album,
    back_populates='bands'
)


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    # Removed BandID
    # BandID = db.Column(db.Integer, db.ForeignKey(
    #     'band.BandID'), nullable=False)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))
    # Add relationship to memberships table
    memberships = db.relationship('Memberships', backref='member', lazy=True)


class Memberships(db.Model):
    MembershipID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'bands.BandID'), nullable=False)
    MemberID = db.Column(db.Integer, db.ForeignKey(
        'members.MemberID'), nullable=False)
    Role = db.Column(db.String(80))
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)




class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)

    bands = db.relationship(
        'Bands',
        secondary=band_album,
        back_populates='albums'
    )
