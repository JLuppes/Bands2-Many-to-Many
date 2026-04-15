# Bands 2 - Many-To-Many - The Sequel to Bands (Now with Many-To-Many Relationships!)

This version of the application starts with the basic band-tracking app [Bands 2](https://github.com/JLuppes/Bands2), which only featured one-to-many relationships (each band can have many members, and many albums, but each member and album can only belong to one band).

We then added a many-to-many relationship between bands and members, so that each member can now belong to many bands. We are also able to track extra information about that relationship, like the member's role in the band and the year they joined and left the band.

The app is set up so that you will then be able to extend the work and add another M:N relationship between bands and albums, so that each album can have many contributing bands. The exact implementation details are left to the developer.

A few things you may want to update as part of your change:

- Model definitions in `model.py`
  - Remove `BandID` from `Album` table
  - Add table for the Band-Album relationship
- The form for adding new albums (doesn't need to include a band)
- New form for adding a Band-Album relationship
- Display pages for bands to include Albums they've contributed to
- Updated navigation links for your new forms and display pages

Some other features you may want to add:

- Display pages for albums that highlights the contributing bands
- Display pages for members that highlights the albums released during their tenure with various bands
- Searchability for the display pages or for the site as a whole

## Running

- Set up a Python virtual environment

  ```bash
  python -m venv venv
  venv\scripts\activate
  ```

- Install project dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Create your `.env` file

  ```bash
  cp .env.example .env
  ```

- Run the app

  ```bash
  flask run --debug
  ```

## Developing Your Own Version

To develop your own version of this project, you can `clone` or `fork` this repo.

- `git clone <repo url>` makes a copy of the repo, but still considers the upstream (parent) repo to be _this_ repo. This is fine for development and testing, but the remote repo still belongs to me.
- Forking the repo makes a copy of the repo on _your_ GitHub account, meaning that you have full control of it from that point forward. This is the better approach when you want to make your own version of an existing project, as opposed to contributing to the original one.
