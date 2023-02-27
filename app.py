import os
from datetime import datetime, date

from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username or email address already exists in DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        existing_email = mongo.db.users.find_one(
            {"email_address": request.form.get("email_address").lower()})

        if existing_user or existing_email:
            flash(f"Username and/or email address already exist.")
            return redirect(url_for("register"))
        # Get input values from Register form
        register = {
            "email_address": request.form.get("email_address").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # Insert new user into DB
        mongo.db.users.insert_one(register)
        # Put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in DB
        existing_user = mongo.db.users.find_one({
            "username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))

            else:
                flash("Incorrect username and/or password.")
                return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Remove user from 'session' cookie
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/contact-us", methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        # Get current date
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")

        if session["user"]:
            # Get input values from Contact form
            message_from_user = {
                "sent_by": session["user"],
                "sent_to": "admin",
                "sent_on": current_date,
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "reason_for_contact": request.form.get("reason_for_contact"),
                "message": request.form.get("message")
            }
            # Insert message into DB
            mongo.db.messages.insert_one(message_from_user)
            flash("Message sent successfully! You can shortly find our reply below, on your Messages section.")
            return redirect(url_for("profile", username=session["user"]))

    return render_template("contact-us.html")


@app.route("/contact-user/<appointment_id>", methods=["GET", "POST"])
def contact_user(appointment_id):
    # Find appointment by ObjectID in DB
    appointment = mongo.db.appointments.find_one({"_id": ObjectId(appointment_id)})
    # Get name of user who created appointment
    user = appointment["created_by"]

    if request.method == "POST":
        # Get current date
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        # Get input values from Contact User form
        message_from_admin = {
            "sent_by": session["user"],
            "sent_to": user,
            "sent_on": current_date,
            "first_name": "bonTeeth",
            "last_name": "staff",
            "reason_for_contact": request.form.get("reason_for_contact"),
            "message": request.form.get("message")
        }
        # Insert message sent by Admin user into DB
        mongo.db.messages.insert_one(message_from_admin)
        flash("Message sent successfully!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("contact-user.html", appointment=appointment)


@app.route("/profile/<username>")
def profile(username):
    # Find username matching 'session' cookie
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


def format_date(datetime_string):
    # Format date to look like '01 January, 2023'
    formatted_datetime = datetime.strptime(datetime_string, "%Y-%m-%d")
    return formatted_datetime.strftime("%d %B, %Y")


@app.route("/profile/<username>/messages")
def messages(username):
    # Find messages in DB
    messages = list(mongo.db.messages.find())
    # Create new list of formatted messages
    formatted_messages = []
    # Iterate through found messages and format 'sent_on' field using format_date function
    for message in messages:
        formatted_message = message
        formatted_message["sent_on"] = format_date(formatted_message["sent_on"])
        formatted_messages.append(formatted_message)

    return render_template("messages.html", username=session["user"], messages=formatted_messages)


@app.route("/delete-message/<message_id>")
def delete_message(message_id):
    # Find message by ObjectId in DB
    mongo.db.messages.delete_one({"_id": ObjectId(message_id)})
    flash("Message deleted successfully.")
    return redirect(url_for("messages", username=session["user"]))


@app.route("/manage-appointments")
def manage_appointments():
    # Find appointments in DB
    appointments = list(mongo.db.appointments.find())
    # Create new list of formatted appointments
    formatted_appointments = []
    # Iterate through found appointments and format 'created_on' and 'requested_date' fields using format_date function
    for appointment in appointments:
        formatted_appointment = appointment
        formatted_appointment["created_on"] = format_date(formatted_appointment["created_on"])
        formatted_appointment["requested_date"] = format_date(formatted_appointment["requested_date"])
        formatted_appointments.append(formatted_appointment)

    return render_template("manage-appointments.html", appointments=formatted_appointments)


@app.route("/book-appointment", methods=["GET", "POST"])
def book_appointment():
    if request.method == "POST":
        # Get current date
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        # Get input values from Book an Appointment form
        appointment = {
            "created_by": session["user"],
            "created_on": current_date,
            "reason_for_visit": request.form.get("reason_for_visit"),
            "requested_date": request.form.get("requested_date"),
            "requested_time": request.form.get("requested_time"),
            "additional_information": request.form.get("additional_information"),
            "status": "pending"
        }
        # Insert new booking into DB
        mongo.db.appointments.insert_one(appointment)
        flash("Appointment booked successfully! Please wait for us to review it and proceed.")
        return redirect(url_for("manage_appointments"))
    # Sort reasons by alphabetical order
    reasons = mongo.db.reason_for_visit.find().sort("reason", 1)
    return render_template("book-appointment.html", reasons=reasons)


@app.route("/edit-appointment/<appointment_id>", methods=["GET", "POST"])
def edit_appointment(appointment_id):
    if request.method == "POST":
        # Get input values from Edit Appointment form
        edited_appointment = {
            "reason_for_visit": request.form.get("reason_for_visit"),
            "requested_date": request.form.get("requested_date"),
            "requested_time": request.form.get("requested_time"),
            "additional_information": request.form.get("additional_information"),
        }
        # Update edited appointment in DB
        mongo.db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": edited_appointment})
        flash("Appointment updated successfully.")
        return redirect(url_for("manage_appointments"))
    # Find appointment by ObjectId in DB
    appointment = mongo.db.appointments.find_one({"_id": ObjectId(appointment_id)})
    # Sort reasons by alphabetical order
    reasons = mongo.db.reason_for_visit.find().sort("reason", 1)
    return render_template("edit-appointment.html", appointment=appointment, reasons=reasons)


@app.route("/cancel-appointment/<appointment_id>")
def cancel_appointment(appointment_id):
    # Update status field to 'cancelled'
    cancelled_appointment = {
        "status": "cancelled"
    }
    # Update status of appointment to 'cancelled' in DB
    mongo.db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": cancelled_appointment})
    flash("Appointment cancelled successfully.")
    return redirect(url_for("manage_appointments"))


@app.route("/accept-appointment/<appointment_id>")
def accept_appointment(appointment_id):
    # Update status field to 'accepted'
    accepted_appointment = {
        "status": "accepted"
    }
    # Update status of appointment to 'accepted' in DB
    mongo.db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": accepted_appointment})
    flash("Appointment accepted successfully.")
    return redirect(url_for("manage_appointments"))


@app.route("/reject-appointment/<appointment_id>")
def reject_appointment(appointment_id):
    # Update status field to 'rejected'
    rejected_appointment = {
        "status": "rejected"
    }
    # Update status of appointment to 'rejected' in DB
    mongo.db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": rejected_appointment})
    flash("Appointment rejected successfully.")
    return redirect(url_for("manage_appointments"))


@app.route("/delete-appointment/<appointment_id>")
def delete_appointment(appointment_id):
    # Delete appointment by ObjectId in DB
    mongo.db.appointments.delete_one({"_id": ObjectId(appointment_id)})
    flash("Appointment deleted successfully.")
    return redirect(url_for("manage_appointments"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
