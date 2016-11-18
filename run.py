__author__ = "Tarun Chhabra"

debug = True
init = True
run = False

if run is True:
    from restapi import app, db
    print "Starting the development server..."
    app.run(debug = True)

elif init is True:
    from restapi import app,db
    print "Creating database.."
    db.create_all()