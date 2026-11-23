from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from model import db, Bands, Members, Albums, Memberships, Albumships,admin
from flask_admin.contrib.sqla import ModelView
import os

# Create our Flask app object
app = Flask(__name__)

# Configure the flask app instance
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)

# Create an instance of SQLAlchemy as our db object
db.init_app(app)

admin.init_app(app)
admin.add_view(ModelView(Bands, db.session, category="Bands"))
admin.add_view(ModelView(Members, db.session, category="Members"))
admin.add_view(ModelView(Albums, db.session, category="Albums"))


# ==========================
# ROUTES
# ==========================

# Home page view


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bands/view')
def view_by_band():
    bands = Bands.query.all()
    memberships = Memberships.query.all()
    albumships = Albumships.query.all()
    albums = Albums.query.all()
    return render_template('display_by_band.html', bands=bands, memberships=memberships,albumships=albumships, albums=albums)


@app.route('/albums/view')
def view_by_album():
    bands = Bands.query.all()
    memberships = Memberships.query.all()
    albumships = Albumships.query.all()
    albums = Albums.query.all()
    return render_template('display_by_album.html', bands=bands,albumships=albumships, albums=albums)


@app.route('/bands/view/<int:id>')
def view_band(id):
    band = Bands.query.get_or_404(id)
    bands = Bands.query.all()
    albumships = Albumships.query.all()
    albums = Albums.query.all()
    return render_template('view_band.html', band=band,bands=bands,albumships=albumships, albums=albums)


@app.route('/bands/add', methods=['GET', 'POST'])
def add_band():
    if request.method == 'POST':
        new_band = Bands(
            BandName=request.form['bandname'],  # type: ignore
            FormedYear=request.form['formedyear'],  # type: ignore
            HomeLocation=request.form['homelocation']  # type: ignore
        )
        db.session.add(new_band)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_band.html')


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    bands = Bands.query.all()  # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form.get('membername'),  # type: ignore
            MainPosition=request.form.get('mainposition')  # type: ignore
            # BandID=request.form['bandid']  # type: ignore
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', bands=bands)


@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],  # type: ignore
            ReleaseYear=request.form['releaseyear'],  # type: ignore
        )
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_album.html', bands=bands)


@app.route('/memberships/add', methods=['GET', 'POST'])
def add_membership():
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        try:
            membership = Memberships(
            BandID = request.form.get('bandid'), # type: ignore
            MemberID = request.form.get('memberid'), # type: ignore
            Role = request.form.get('role'), # type: ignore
            StartYear = request.form.get('startyear') or None, # type: ignore
            EndYear = request.form.get('endyear') or None  # type: ignore
            )

            db.session.add(membership)
            db.session.commit()

            return redirect(url_for('view_by_band'))
        
        except Exception as e:
            db.session.rollback()
            error = f"Error adding new membership: {e}"
            return render_template('add_membership.html', bands=bands,
                                   members=members, error=error)
        
    return render_template('add_membership.html', bands=bands,
                           members=members)

@app.route('/albumships/add', methods=['GET', 'POST'])
def add_albumship():
    bands = Bands.query.all()
    albums = Albums.query.all()
    if request.method == 'POST':
        try:
            id = request.form.get('albumid')
            album = Albums.query.filter_by(AlbumID = id).first()

            albumship = Albumships(
            BandID = request.form.get('bandid'), # type: ignore
            AlbumID = id, # type: ignore
            Title = album.AlbumTitle,  # type: ignore
            Release = album.ReleaseYear # type: ignore
            )

            db.session.add(albumship)
            db.session.commit()

            return redirect(url_for('view_by_band'))
        
        except Exception as e:
            db.session.rollback()
            error = f"Error adding new albumships: {e}"
            return render_template('add_albumships.html', bands=bands,
                                   albums=albums, error=error)
        
    return render_template('add_albumships.html', bands=bands,
                           albums=albums)


@app.route('/memberships/edit/<int:id>', methods=['GET', 'POST'])
def edit_membership(membership_id):
    membership = Memberships.query.get_or_404(membership_id)
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership.MembershipID = request.form.get('membership_id')
        membership.BandID = request.form.get('bandid')
        membership.MemberID = request.form.get('memberid')
        membership.Role = request.form.get('role')
        membership.StartYear = request.form.get('startyear') or None
        membership.EndYear = request.form.get('endyear') or None
        db.session.commit()
        # flash('Membership updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_membership.html', membership=membership, bands=bands,
    members=members)


@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    # flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))

# Create DB and tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app if this file is launched via Python (instead of flask run --debug)
if __name__ == '__main__':
    app.run(debug=True)
