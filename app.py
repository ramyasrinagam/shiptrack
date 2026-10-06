from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "hackathon_ultimate_key_2026"

# All users share the same common password: password123
users = {
    "customer.logistics@gmail.com": {
        "password": "password123",
        "role": "Customer",
        "name": "Rahul Varma",
    },
    "manager.head@gmail.com": {
        "password": "password123",
        "role": "Manager",
        "name": "Vikramaditya (Operations Head)",
    },
    "driver.agent@gmail.com": {
        "password": "password123",
        "role": "Driver",
        "name": "Ramesh Kumar",
    },
    "support.helpdesk@gmail.com": {
        "password": "password123",
        "role": "Customer Care",
        "name": "Priya Sharma (Lead Support)",
    },
}

shipments = {
    "TRK123": {
        "status": "Out for Delivery",
        "origin": "Hyderabad Hub",
        "destination": "Warangal Campus",
        "order_date": "2026-10-02 10:30 AM",
        "est_delivery": "2026-10-06 04:00 PM",
        "location": "Warangal Bypass Road, Telangana",
        "driver_name": "Ramesh Kumar",
        "driver_phone": "+91 98765 43210",
        "driver_vehicle": "TS 08 AB 1234 (Mini Truck)",
        "driver_photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=faces",
        "support_ticket": "Ticket #9021 - Address Verified",
        "timeline": [
            {"date": "Oct 02, 10:30 AM", "event": "Order Placed Successfully"},
            {"date": "Oct 03, 02:00 PM", "event": "Shipped from Hyderabad Hub"},
            {"date": "Oct 05, 08:00 AM", "event": "Arrived at Regional Facility"},
            {"date": "Oct 06, 09:00 AM", "event": "Out for Delivery with Agent"},
        ],
    },
    "TRK456": {
        "status": "In Transit",
        "origin": "Vizag Port",
        "destination": "Vijayawada Logistics Park",
        "order_date": "2026-10-04 01:15 PM",
        "est_delivery": "2026-10-07 02:00 PM",
        "location": "Eluru Highway Checkpost, AP",
        "driver_name": "Kiran Abbavaram",
        "driver_phone": "+91 91234 56789",
        "driver_vehicle": "AP 39 Z 9988 (Heavy Cargo)",
        "driver_photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=faces",
        "support_ticket": "Ticket #8841 - Custom Clearance Done",
        "timeline": [
            {"date": "Oct 04, 01:15 PM", "event": "Container Booked"},
            {"date": "Oct 05, 06:00 AM", "event": "Departed Vizag Port Terminal"},
            {"date": "Oct 06, 11:00 AM", "event": "Passed Eluru Checkpost"},
        ],
    },
    "TRK789": {
        "status": "Processing",
        "origin": "Bengaluru Hub",
        "destination": "Tirupati Temple City",
        "order_date": "2026-10-05 09:00 AM",
        "est_delivery": "2026-10-08 06:00 PM",
        "location": "Electronic City Sorting Facility, BLR",
        "driver_name": "Subbaraju",
        "driver_phone": "+91 99887 76655",
        "driver_vehicle": "KA 01 EF 5678 (Electric Van)",
        "driver_photo": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=200&h=200&fit=crop&crop=faces",
        "support_ticket": "Ticket #7712 - Express Dispatch Requested",
        "timeline": [
            {"date": "Oct 05, 09:00 AM", "event": "Package Received at BLR Hub"},
            {"date": "Oct 06, 10:00 AM", "event": "Quality Check Passed & Tagged"},
        ],
    },
}


@app.route("/")
def home():
  if "user" not in session or not session.get("otp_verified"):
    return redirect(url_for("login"))
  role = session.get("role")
  user_email = session.get("user")
  user_name = users[user_email]["name"]
  return render_template(
      "index.html",
      role=role,
      user_email=user_email,
      user_name=user_name,
      shipments=shipments,
  )


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    if email in users and users[email]["password"] == password:
      session["user"] = email
      session["role"] = users[email]["role"]
      session["otp_verified"] = False
      return redirect(url_for("verify_otp"))
    return render_template("login.html", error="Invalid Gmail or Password!")
  return render_template("login.html")


@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
  if "user" not in session:
    return redirect(url_for("login"))
  if request.method == "POST":
    if request.form.get("otp") == "4829":
      session["otp_verified"] = True
      return redirect(url_for("home"))
    return render_template("otp.html", error="Wrong OTP! Use 4829")
  return render_template("otp.html")


@app.route("/track", methods=["POST"])
def track():
  if "user" not in session or not session.get("otp_verified"):
    return redirect(url_for("login"))
  tracking_id = request.form.get("tracking_id", "").strip().upper()
  return render_template(
      "index.html",
      role=session.get("role"),
      user_email=session.get("user"),
      user_name=users[session.get("user")]["name"],
      shipment=shipments.get(tracking_id),
      tracking_id=tracking_id,
      shipments=shipments,
  )


@app.route("/update-status", methods=["POST"])
def update_status():
  if "user" not in session:
    return redirect(url_for("login"))
  tid = request.form.get("tracking_id")
  status = request.form.get("status")
  loc = request.form.get("location")
  if tid in shipments:
    if status:
      shipments[tid]["status"] = status
    if loc:
      shipments[tid]["location"] = loc
  return redirect(url_for("home"))


@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))


if __name__ == "__main__":
  app.run(debug=True)