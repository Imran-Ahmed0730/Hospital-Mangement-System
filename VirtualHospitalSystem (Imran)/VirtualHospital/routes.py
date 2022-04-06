from VirtualHospital import app
from flask import render_template, redirect, url_for, flash, request
from VirtualHospital.models import Doctor, Patients
from VirtualHospital.forms import SignUpForm, DoctorSignUpForm, SignInForm, SignInFormDoctor, RemovePatientForm, AppointmentForm, symptomForm, FeedbackForm, UpdateMedicationForm
from VirtualHospital import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    return render_template('home.html')


@app.route('/homeD')
@login_required
def homeD_page():
    return render_template('homeD.html')

@app.route('/DoctorList')
def Doctor_List():
    doctors = Doctor.query.all()
    return render_template('DoctorList.html', doctors=doctors)

@app.route('/Doctors', methods=['GET', 'POST'])
def Available_Doctors():
    appointment_form = AppointmentForm()
    if request.method == "POST":
        appointed_doctor = request.form.get('appointed_doctor')
        a_doctor_object = Doctor.query.filter_by(username=appointed_doctor).first()
        if a_doctor_object:
            if current_user.can_appoint(a_doctor_object):
                a_doctor_object.appoint(current_user)
                flash(f'Appointment For Dr. {a_doctor_object.username}',category='success')
            else:
                flash(f"Couldn't Confirm Appointment (Either you already have conformed an Appointment or you don't have enough money for the Appointment!!",category='danger')

        return redirect(url_for('appointment_page'))
    if request.method == "GET":
        doctors = Doctor.query.all()
        return render_template('AvailableDoctors.html', doctors=doctors, appointment_form=appointment_form)

@app.route('/PatientList', methods=['GET', 'POST'])
def Patient_List():
    remove_patient_form = RemovePatientForm()
    #new content:10-12-21
    if request.method == "POST":
        removed_patient = request.form.get('removed_patient')
        a_patient_object = Patients.query.filter_by(username=removed_patient).first()
        if a_patient_object:
            if a_patient_object.owner_id == current_user.id:
                a_patient_object.owner_id = None
                db.session.commit()
                flash(f'{a_patient_object.username} Has Been Removed successfully!!',category='success')
        return redirect(url_for('Patient_List'))
    if request.method == "GET":
        patients = Patients.query.all()
        return render_template('PatientList.html', patients=patients, remove_patient_form=remove_patient_form)
    #End new content

@app.route('/')
@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html')

@app.route('/Aboutus')
def about_us_page():
    return render_template('AboutUs.html')
@app.route('/Appointment', methods=['GET', 'POST'])
def appointment_page():
    form = symptomForm()
    attempted_patient = Patients.query.filter_by(username=current_user.username).first()
    attempted_patient.symptom = form.symptom.data
    db.session.commit()
    return render_template('AppointmentPage.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignUpForm()
    if form.validate_on_submit():
        patient_to_create = Patients(username=form.username.data,
                                     age= form.age.data,
                                     email_address=form.email_address.data,
                                     p_num=form.p_num.data,
                                     password=form.password1.data)
        db.session.add(patient_to_create)
        db.session.commit()
        flash(f'You Have Successfully Signed Up. Please Sign In to Continue!!', category='success')
        return redirect(url_for('signin_patient_page'))
    if form.errors != {}:  # if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a patient user: {err_msg}', category='danger')

    return render_template('signup.html', form=form)


@app.route('/DoctorSignup', methods=['GET', 'POST'])
def doctor_signup_page():
    form = DoctorSignUpForm()
    if form.validate_on_submit():
        doctor_to_create = Doctor(id=form.id.data,
                                  username=form.username.data,
                                  email=form.email.data,
                                  clas=form.clas.data,
                                  password=form.password1.data,
                                  experience=form.experience.data,
                                  phone_number=form.phone_number.data
                                  )
        db.session.add(doctor_to_create)
        db.session.commit()
        flash(f'You Have Successfully Signed Up. Please Sign In to Continue!!', category='success')
        return redirect(url_for('signin_doctor_page'))
    if form.errors != {}:  # if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an creating a doctor user: {err_msg}', category='danger')
    return render_template('signupD.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin_patient_page():
    form = SignInForm()
    if form.validate_on_submit():
        attempted_patient = Patients.query.filter_by(username=form.username.data).first()
        if attempted_patient and attempted_patient.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_patient)
            flash(f'You are successfully logged in as {attempted_patient.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not matched! Please try again', category='danger')

    return render_template('signin.html', form=form)


@app.route('/DoctorSignin', methods=['GET', 'POST'])
def signin_doctor_page():
    form = SignInFormDoctor()
    if form.validate_on_submit():
        attempted_Doctor = Doctor.query.filter_by(username=form.username.data).first()
        if attempted_Doctor and attempted_Doctor.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_Doctor)
            flash(f'You are successfully logged in as {attempted_Doctor.username}', category='success')
            return redirect(url_for('homeD_page'))
        else:
            flash('Username and password are not matched! Please try again', category='danger')
    return render_template('signinD.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out successfully!", category='info')
    return redirect(url_for('welcome_page'))

@app.route('/doctorProfile')
def doctor_profile_page():
    return render_template('Doctor_Profile.html')

@app.route('/patientProfile')
def patient_profile_page():
    return render_template('Patient_Profile.html')

@app.route('/appointmentinfo')
def appointment_info():
    return render_template('Appointment_Info.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    attempted_patient = Patients.query.filter_by(username=current_user.username).first()
    attempted_patient.owner_feedback = form.owner_feedback.data
    db.session.commit()
    return render_template('Feedback.html', form=form)

"""@app.route('/UpdateMedication')
def update_medication():
    return render_template('UpdateMedication.html')"""

@app.route('/UpdateMedication', methods=['GET', 'POST'])
@login_required
def Update_medication():
    selectForm = UpdateMedicationForm()
    selected_patient = request.form.get('patient_select')
    if request.method == "POST":
        patient_to_update = Patients.query.filter_by(username=selected_patient).first()
        if patient_to_update:
            if selectForm.validate_on_submit():
                patient_to_update.medicine = selectForm.medication.data
                patient_to_update.dose = selectForm.dose.data
                db.session.commit()
                flash(f"You have successfully updated {patient_to_update.username}'s medication!", category='success')
                return redirect(url_for('homeD_page'))

    if request.method == "GET":
        patientList = Patients.query.filter_by(owner_id=current_user.id)
        return render_template('UpdateMedication.html', patientList=patientList, selectForm=selectForm)

@app.route('/feedback')
def feedback_page():
    patients = Patients.query.all()
    return render_template('Feedback_page.html', patients=patients)

