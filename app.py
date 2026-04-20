from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from model import db, Bands, Members, Albums, Memberships, admin
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
admin.add_view(ModelView(Memberships, db.session, category="Members"))
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
    return render_template('display_by_band.html', bands=bands, memberships=memberships)


@app.route('/bands/view/<int:id>')
def view_band(id):
    band = Bands.query.get_or_404(id)
    memberships = Memberships.query.all()
    return render_template('view_band.html', band=band, memberships=memberships)


@app.route('/members/view')
def view_by_member():
    members = Members.query.all()
    memberships = Memberships.query.all()
    return render_template('display_by_member.html', members=members, memberships=memberships)


@app.route('/members/view/<int:id>')
def view_member(id):
    member = Members.query.get_or_404(id)
    memberships = Memberships.query.all()
    return render_template('view_member.html', member=member, memberships=memberships)


@app.route('/bands/add', methods=['GET', 'POST'])
def add_band():
    if request.method == 'POST':
        new_band = Bands(
            BandName=request.form['bandname'],
            FormedYear=request.form['formedyear'],
            HomeLocation=request.form['homelocation']
        )
        db.session.add(new_band)
        db.session.commit()
        return redirect(url_for('view_by_band'))
    return render_template('add_band.html')


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    bands = Bands.query.all()  # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('view_by_member'))
    return render_template('add_member.html', bands=bands)


@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()

    if request.method == 'POST':
        title = request.form['title']
        year = request.form.get('releaseyear') or None
        band_ids = request.form.getlist('bands')

        album = Albums(
            AlbumTitle=title,
            ReleaseYear=year
        )

        for bid in band_ids:
            band = Bands.query.get(int(bid))
            if band:
                album.bands.append(band)

        db.session.add(album)
        db.session.commit()

        return redirect(url_for('view_by_band'))

    return render_template('add_album.html', bands=bands)


@app.route('/memberships/add', methods=['GET', 'POST'])
def add_membership():
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        try:
            membership = Memberships(
                BandID=request.form.get('bandid'),
                MemberID=request.form.get('memberid'),
                Role=request.form.get('role'),
                StartYear=request.form.get('startyear') or None,
                EndYear=request.form.get('endyear') or None
            )
            db.session.add(membership)
            db.session.commit()
            # flash('Membership assigned', 'success')
            return redirect(url_for('view_by_band'))
        except Exception as e:
            db.session.rollback()
            error = f"Error adding new membership: {e}"
            return render_template('add_membership.html', bands=bands, members=members, error=error)
    return render_template('add_membership.html', bands=bands, members=members)


@app.route('/memberships/edit/<int:id>', methods=['GET', 'POST'])
def edit_membership(id):
    membership = Memberships.query.get_or_404(id)
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership.BandID = request.form.get('bandid')
        membership.MemberID = request.form.get('memberid')
        membership.Role = request.form.get('role')
        membership.StartYear = request.form.get('startyear') or None
        membership.EndYear = request.form.get('endyear') or None
        db.session.commit()
        # flash('Membership updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_membership.html', membership=membership, bands=bands, members=members)


@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    # flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))


@app.route('/bands/edit/<int:band_id>', methods=['GET', 'POST'])
def edit_band(band_id):
    band = Bands.query.get_or_404(band_id)

    if request.method == 'POST':
        try:

            band.BandName = request.form.get('bandname')
            band.FormedYear = request.form.get('formedyear')
            band.HomeLocation = request.form.get('homelocation')

            db.session.add(band)
            db.session.commit()
            return redirect(url_for('view_by_band'))

        except Exception as e:
            db.session.rollback()
            error = f"Error updating band: {e}"
            return render_template('edit_band.html', band=band, error=error)

    return render_template('edit_band.html', band=band)


@app.route('/bands/delete/<int:band_id>')
def delete_band(band_id):
    band = Bands.query.get_or_404(band_id)

    try:
        db.session.delete(band)
        db.session.commit()
        return redirect(url_for('view_by_band'))
    except Exception as e:
        db.session.rollback()
        error = f"Error deleting band: {e}"
        return redirect(url_for('view_by_band'))


# Create DB and tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app if this file is launched via Python (instead of flask run --debug)
if __name__ == '__main__':
    app.run(debug=True)
