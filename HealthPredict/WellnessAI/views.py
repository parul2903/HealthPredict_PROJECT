from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Appointment, Contact, Profile, SymptomDetail, Doctor, UserDetail, HealthData, updateData
from django.http import JsonResponse
import joblib
from django.shortcuts import render
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
from django.contrib import messages
from .models import BlogPost

class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'

# Create your views here.
def home(request):
    recent_posts = BlogPost.objects.all().order_by('-pub_date')[:2]  # Get the 2 most recent posts
    return render(request, 'home.html', {'recent_posts': recent_posts})

def about(request):
    return render(request, 'about.html', {})

def symptomChecker(request):
    return render(request, 'symptomChecker.html',{})

def contact(request):
    return render(request, 'contact.html',{})

def register(request):
    if request.method == 'POST':
       username = request.POST['username'] 
       email = request.POST['email'] 
       password = request.POST['password'] 
       user = User.objects.create(username=username,email=email,password=make_password(password))
       user.save()
       return redirect('login')
    else:
        return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(username=username,password=password)
        # print(user)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            return redirect('login')
    else:
        return render(request,'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage after logout

def profile(request):
    return render(request, 'profile.html')

def profile_view(request):
    # Handle user profile logic here
    return render(request, 'profile.html')


@login_required
def make_appointment(request):
    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        phone = request.POST.get('phone')

        # Save the appointment to the database (make sure you have an Appointment model)
        appointment = Appointment(
            doctor=doctor, 
            name=name, 
            email=email, 
            date=date, 
            time=time, 
            phone=phone,
            user=request.user
        )
        appointment.save()


        # Return a JSON response with the appointment details
        return JsonResponse({
            'doctor': doctor,
            'name': name,
            'email': email,
            'date': date,
            'time': time,
            'phone': phone
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the contact form data to the database
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        
        # Return a JSON response
        return JsonResponse({'success': True})

    return render(request, 'contact.html')  # Return the contact page


# def symptom_checker(request):
#     if request.method == 'POST':
#         symptoms = request.POST.getlist('symptom[]')
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         duration = request.POST.get('duration')

#         # Process the symptoms and return a diagnosis (this part can be expanded with ML or database logic)
#         # For now, let's just return the inputs as a JSON response to demonstrate

#         response_data = {
#             'symptoms': symptoms,
#             'age': age,
#             'gender': gender,
#             'duration': duration,
#             'diagnosis': 'Possible conditions will be listed here'
#         }

#         return JsonResponse(response_data)

#     return render(request, 'symptom_checker.html')


# # Handle the first form (Age and Gender)
# def symptom_checker_info(request):
#     if request.method == 'POST':
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         request.session['age'] = age
#         request.session['gender'] = gender
#         return render(request, 'symptomInput.html')

#     return render(request, 'symptomChecker.html')

# # Handle symptom input and prediction
# def symptom_checker_results(request):
#     if request.method == 'POST':
#         symptoms = request.POST.get('symptoms')

#         # Convert symptoms into the format needed for your model
#         symptoms_list = symptoms.split(',')
#         symptoms_cleaned = [symptom.strip() for symptom in symptoms_list]
        
#         # Assuming your model uses a one-hot encoding of symptoms, you need to convert the symptoms to a binary vector
#         # Example: converting the symptoms into a format understood by the model
#         symptom_vector = create_symptom_vector(symptoms_cleaned)
        
#         # Pass the vector to the model and get the predictions
#         predicted_disease = model.predict([symptom_vector])
#         top_10_predictions = model.predict_proba([symptom_vector])

#         # Prepare the top 10 conditions with probabilities
#         top_conditions = get_top_conditions_with_scores(top_10_predictions)

#         # Render the result page
#         return render(request, 'result.html', {
#             'predicted_disease': predicted_disease[0], 
#             'top_diseases': top_conditions
#         })

#     return render(request, 'symptomInput.html')

# # Utility functions
# def create_symptom_vector(symptoms):
#     # Example of converting symptoms into a one-hot encoded vector
#     # (You'll need to adapt this based on how your model was trained.)
#     all_symptoms = ['fever', 'cough', 'fatigue', 'headache', 'nausea', 'vomiting']  # Add all possible symptoms here
#     symptom_vector = [1 if symptom in symptoms else 0 for symptom in all_symptoms]
#     return symptom_vector

# def get_top_conditions_with_scores(predictions):
#     # This function assumes that `predictions` is an array of probabilities for each possible disease.
#     # You would map the probabilities to the disease names.
    
#     # Example placeholder: this could be based on your model's class labels
#     disease_labels = ['Flu', 'Common Cold', 'COVID-19', 'Pneumonia', 'Allergy']  # Replace with actual disease names
    
#     # Sort and pick top 10 diseases
#     top_conditions = sorted(zip(disease_labels, predictions[0]), key=lambda x: -x[1])[:10]
    
#     return top_conditions

# Load the saved model and symptom encoder
with open('C:/Users/Parul/Documents/TRIMESTER 4/TRI4_PROJECT__FINAL/HealthPredict_PROJECT/HealthPredict/WellnessAI/symptom_checker_model.pkl', 'rb') as f:
    clf = pickle.load(f)

# Example symptoms encoder (you would load your actual MultiLabelBinarizer)
mlb = MultiLabelBinarizer()
mlb.fit([['Cough', 'Fever', 'Fatigue', 'Sore Throat', 'Shortness of Breath', 'Runny Nose']])

def symptom_checker(request):
    if request.method == 'POST':
        # Extract the user's selected symptoms from the form
        selected_symptoms = request.POST.getlist('selectedSymptoms[]')

        # Predict the top 5 diseases
        input_data = mlb.transform([selected_symptoms])
        probabilities = clf.predict_proba(input_data)[0]
        top_5_indices = np.argsort(probabilities)[-5:][::-1]
        top_5_diseases = clf.classes_[top_5_indices]
        top_5_probabilities = probabilities[top_5_indices]

        # Prepare the context for the result page
        context = {
            'predictions': zip(top_5_diseases, top_5_probabilities)
        }
        return render(request, 'result.html', context)

    return render(request, 'symptomChecker.html')


# from django.shortcuts import render, redirect
# from .models import BasicDetails, Symptom, Condition
# from .forms import BasicDetailsForm, SymptomForm

# # Step 1: Basic Details View
# def basic_details_view(request):
#     if request.method == 'POST':
#         form = BasicDetailsForm(request.POST)
#         if form.is_valid():
#             basic_details = form.save()
#             request.session['basic_id'] = basic_details.id  # Store ID for later steps
#             return redirect('symptoms')  # Go to the next step
#     else:
#         form = BasicDetailsForm()
#     return render(request, 'symptom_checker/basic_details.html', {'form': form})


## NEW
# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import UserDetail, SymptomDetail
from .ml_model import predict_disease  # Import ML prediction function

@login_required
def symptom_checker(request):
    if request.user.is_authenticated:
        # The user is logged in
        user = request.user  # You can now access user-specific data
        # Perform operations related to the logged-in user
    else:
        # Redirect to login page if the user is not logged in
        return redirect('login')
    
    return render(request, 'symptom_checker.html', {'user': user})

# @login_required
# def symptom_checker(request):
#     # Only logged-in users can reach this point, so request.user is always valid here.
#     if request.method == 'POST':
#         symptom = request.POST.get('symptom')
#         prediction = some_prediction_logic(symptom)  # Replace with actual prediction logic

#         # Here, we use request.user to link the prediction to the logged-in user
#         SymptomDetail.objects.create(
#             user=request.user,  # Associate prediction with the logged-in user
#             symptom=symptom,
#             prediction=prediction
#         )
        
#         return redirect('profile')  # Redirect to profile to show updated predictions
#     return render(request, 'symptomChecker.html')

def save_user_details(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # Link UserDetail to the logged-in Django user
        user_detail, created = UserDetail.objects.get_or_create(
            user=request.user,
            defaults={'age': age, 'gender': gender}
        )
        
        return JsonResponse({'user_id': user_detail.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)
        
    #     # Save user details and return a user ID
    #     user = UserDetail.objects.create(age=age, gender=gender)
    #     return JsonResponse({'user_id': user.id})
    # return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_prediction(request):
    if request.method == 'POST':
        # user_id = request.POST.get('user_id')
        user = request.user
        # Ensure that UserDetail exists for this user
        user_detail, created = UserDetail.objects.get_or_create(user=user)
        symptoms = request.POST.getlist('symptoms[]')  # Symptoms sent as an array
        
        # Predict the disease based on symptoms
        predicted_disease = predict_disease(symptoms)
        
        # Mock description for demonstration; ideally, pull from a database or API
        disease_descriptions = {
    "Flu": "Influenza, commonly known as the flu, is an infectious disease caused by the influenza virus.",
    "Cold": "A common viral infection of the upper respiratory tract, primarily the nose and throat.",
    "Asthma": "A condition in which your airways narrow and swell, producing extra mucus.",
    "Migraine": "A severe headache often accompanied by nausea and sensitivity to light and sound.",
    "Tuberculosis": "A serious infectious disease that mainly affects the lungs but can also affect other parts of the body.",
    "Influenza": "Influenza, commonly known as the flu, is an infectious disease caused by the influenza virus.",
    "Dehydration": "A condition that occurs when the body loses more fluids than it takes in.",
    "Chronic Stress": "A state of ongoing physiological response to stressors that can affect health.",
    "Glaucoma": "A group of eye conditions that damage the optic nerve, often associated with increased pressure in the eye.",
    "Heart Failure": "A chronic condition where the heart doesn't pump blood as well as it should.",
    "Eczema": "A condition that makes your skin red and itchy, often chronic and inflammatory.",
    "Common Cold": "A common viral infection of the upper respiratory tract, primarily the nose and throat.",
    "Attention Deficit Disorder": "A neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity.",
    "Hypoglycemia": "A condition caused by an abnormally low level of blood sugar (glucose).",
    "Hypothyroidism": "A condition where the thyroid gland does not produce enough thyroid hormones.",
    "Arthritis": "An inflammation of one or more joints, causing pain and stiffness.",
    "Urinary Tract Infection": "An infection in any part of the urinary system, including kidneys, bladder, or urethra.",
    "Bronchitis": "An inflammation of the lining of the bronchial tubes, causing cough and mucus production.",
    "Insomnia": "A sleep disorder characterized by difficulty falling and/or staying asleep.",
    "Gastroenteritis": "An inflammation of the stomach and intestines, often caused by viral or bacterial infection.",
    "Viral Fever": "A fever caused by a viral infection, often accompanied by other symptoms like fatigue and body aches.",
    "Anemia": "A condition where you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
    "Iron Deficiency": "A condition where the body doesn't have enough iron, leading to anemia and fatigue.",
    "Photophobia": "A condition characterized by an increased sensitivity to light, often associated with eye problems.",
    "Peripheral Neuropathy": "A result of damage to the peripheral nerves, causing weakness, numbness, and pain.",
    "Food Poisoning": "An illness caused by consuming contaminated food or beverages.",
    "Irritable Bowel Syndrome": "A common disorder affecting the large intestine, characterized by cramping, abdominal pain, and changes in bowel habits.",
    "Strep Throat": "A bacterial infection that causes inflammation and pain in the throat.",
    "Panic Attack": "A sudden episode of intense fear or anxiety that triggers severe physical reactions.",
    "Psoriasis": "A chronic autoimmune condition that causes rapid skin cell production, leading to scaling and inflammation.",
    "Anaphylaxis": "A severe, potentially life-threatening allergic reaction that can occur rapidly.",
    "Tension Headache": "A common type of headache characterized by a dull, aching sensation and tightness.",
    "Malaria": "A disease caused by a parasite transmitted through the bite of infected mosquitoes, characterized by fever, chills, and flu-like symptoms.",
    "Mononucleosis": "A viral infection characterized by extreme fatigue, fever, and sore throat, often caused by the Epstein-Barr virus.",
    "Cervical Spondylosis": "A condition caused by age-related wear and tear on the spinal disks in the neck.",
    "Ear Infection": "An infection of the ear, often associated with pain and sometimes hearing loss.",
    "Diabetes": "A chronic disease that occurs when the body cannot effectively use insulin or produce enough insulin.",
    "Acid Reflux": "A condition where stomach acid flows back into the esophagus, causing heartburn and discomfort.",
    "Rotator Cuff Injury": "An injury to the muscles and tendons that stabilize the shoulder joint.",
    "Tonsillitis": "An infection or inflammation of the tonsils, often causing a sore throat and difficulty swallowing.",
    "Sinus Infection": "An infection or inflammation of the sinus cavities, leading to congestion, pressure, and discomfort.",
    "Seborrheic Dermatitis": "A skin condition causing scaly patches, red skin, and stubborn dandruff.",
    "Meniscus Tear": "A tear in the cartilage of the knee, often causing pain, swelling, and limited range of motion.",
    "Conjunctivitis": "An inflammation of the outer membrane of the eyeball and the inner eyelid, often causing redness and discharge.",
    "Chickenpox": "A highly contagious viral infection characterized by an itchy rash and flu-like symptoms.",
    "Sciatica": "Pain that radiates along the path of the sciatic nerve, typically affecting one side of the body.",
    "Laryngitis": "An inflammation of the larynx, causing hoarseness or loss of voice.",
    "Endocarditis": "An infection of the inner lining of the heart chambers and valves.",
    "Prostatitis": "An inflammation of the prostate gland, often causing pain and urinary issues.",
    "Vertigo": "A sensation of spinning or dizziness, often caused by issues in the inner ear or brain.",
    "Oral Thrush": "A fungal infection in the mouth, characterized by white patches and soreness.",
    "Fibromyalgia": "A condition characterized by widespread musculoskeletal pain, fatigue, and sleep disturbances.",
    "Deep Vein Thrombosis": "A condition where a blood clot forms in a deep vein, typically in the legs, causing pain and swelling.",
    "Plantar Fasciitis": "An inflammation of the tissue that runs across the bottom of the foot, causing heel pain.",
    "Depression": "A mood disorder that causes a persistent feeling of sadness and loss of interest.",
    "Bipolar Disorder": "A mental health condition characterized by extreme mood swings, including emotional highs and lows.",
    "Pulmonary Embolism": "A blockage in one of the pulmonary arteries in the lungs, often caused by blood clots.",
    "Allergic Rhinitis": "An allergic reaction that causes sneezing, runny nose, and itchy eyes.",
    "Gingivitis": "A common and mild form of gum disease that causes irritation, redness, and swelling.",
    "Chronic Obstructive Pulmonary Disease (COPD)": "A progressive lung disease that makes it hard to breathe due to obstructed airflow.",
    "Pneumonia": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid.",
    "Anxiety": "A mental health condition characterized by feelings of worry, anxiety, or fear that interfere with daily activities.",
    "Dry Mouth Syndrome": "A condition characterized by a lack of saliva in the mouth, leading to dryness and discomfort.",
    "Seasonal Allergies": "Allergies that occur at certain times of the year, often triggered by pollen from trees, grasses, or weeds.",
    "Bronchitis": "An inflammation of the lining of the bronchial tubes, causing cough and mucus production.",
    "Generalized Anxiety Disorder": "A disorder characterized by excessive anxiety and worry about various aspects of life.",
    "Migraine": "A severe headache often accompanied by nausea and sensitivity to light and sound.",
    "Sinusitis": "An infection or inflammation of the sinus cavities, leading to congestion, pressure, and discomfort.",
    "Panic Disorder": "A type of anxiety disorder characterized by recurrent panic attacks.",
    "Emphysema": "A lung condition that causes shortness of breath due to the gradual damage of lung tissue."
}
        description = disease_descriptions.get(predicted_disease, "No description available.")
        
        # Save symptoms and prediction
        # user = UserDetail.objects.get(id=user_id)
        symptom_detail = SymptomDetail.objects.create(
            user=user,
            symptoms=", ".join(symptoms),
            predicted_disease=predicted_disease,
            description=description
        )
        print(f"SymptomDetail created: {symptom_detail}")
        
        # Return the prediction data
        return JsonResponse({
            'predicted_disease': predicted_disease,
            'description': description,
            'symptoms': symptoms,
            'user_detail': {
                'age': user_detail.age,
                'gender': user_detail.gender}
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)





# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor

def add_doctor(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # Create and save a new doctor instance
        doctor = Doctor(name=name, specialization=specialization, phone=phone,
                        email=email, experience=experience, address=address, image=image)
        doctor.save()

        # Success message
        messages.success(request, 'The doctor has been added successfully.')

        # Redirect to doctor list page
        return redirect('doctor_list')

    return render(request, 'add_doctor.html')

def doctor_list(request):
    # Retrieve all doctors
    # doctors = Doctor.objects.all()
    # return render(request, 'doctor_list.html', {'doctors': doctors})

    query = request.GET.get('search')
    if query:
        doctors = Doctor.objects.filter(name__icontains=query) | Doctor.objects.filter(specialization__icontains=query)
    else:
        doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


# views.py
from django.shortcuts import get_object_or_404

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})


def doctor_list(request):
    search_query = request.GET.get('search', '')
    doctors = Doctor.objects.all()
    if search_query:
        doctors = doctors.filter(name__icontains=search_query) | doctors.filter(specialization__icontains=search_query)
    return render(request, 'doctor_list.html', {'doctors': doctors})


#### USER DASHBOARD
# import datetime
# @login_required
# def user_dashboard(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     appointments = Appointment.objects.filter(name=user.username)  # Filter based on the user's name
#     symptoms = SymptomDetail.objects.filter(user=user.profile.userdetail)

#     # Calculations for KPIs
#     upcoming_appointments = appointments.filter(date__gte=datetime.today()).count()
#     symptom_severity = 4.5  # Placeholder; replace with actual calculation if needed.

#     context = {
#         'user': user,
#         'profile': profile,
#         'appointments': appointments,
#         'upcoming_appointments': upcoming_appointments,
#         'symptoms': symptoms,
#         'symptom_severity': symptom_severity,
#     }
#     return render(request, 'profile.html', context)

# @login_required
# def dashboard(request):
#     user_profile = UserDetail.objects.get(user=request.user)
#     appointments = Appointment.objects.filter(user=request.user)
#     symptoms = SymptomDetail.objects.filter(user=request.user)

#     # Calculate any KPIs if needed
#     upcoming_appointments = appointments.count()  # example KPI
#     symptom_severity = symptoms.count()  # placeholder for severity metric

#     context = {
#         'user': request.user,
#         'profile': user_profile,
#         'appointments': appointments,
#         'symptoms': symptoms,
#         'upcoming_appointments': upcoming_appointments,
#         'symptom_severity': symptom_severity,
#     }
#     return render(request, 'profile.html', context)



# @login_required
# def user_dashboard(request):
#     # Fetch SymptomDetail records for the logged-in user
#     symptoms = SymptomDetail.objects.filter(user=request.user)
#     print(f"Symptoms for user {request.user}: {symptoms}")
#     # Pass the symptom records to the template
#     return render(request, 'profile.html', {'symptoms': symptoms})

from django.utils import timezone
@login_required
def user_dashboard(request):

    # Get the current date in the user's timezone
    today = timezone.localdate(timezone.now())

    # Fetch SymptomDetail records for the logged-in user
    symptoms = SymptomDetail.objects.filter(user=request.user)

    # Fetch Appointment records for the logged-in user
    appointments = Appointment.objects.filter(user=request.user)
    
    # Query for upcoming appointments
    upcoming_appointments = Appointment.objects.filter(date__gte=today).count()

    print("Today's Date:", today)
    appointments = Appointment.objects.filter(date__gte=today)
    print("Appointments:", appointments)

    health_data = updateData.objects.filter(user=request.user)
    
    if health_data:
        # Get the first (most recent) health data
        health_data = health_data[0]
        exercise_frequency = health_data.exercise_frequency
        diet_quality = health_data.diet_quality
        sleep_hours = health_data.sleep_hours
        # name = health_data.name
        # phone = health_data.phone
        # address = health_data.address
        # gender = health_data.gender
        # weight = health_data.weight
        
    else:
        # Default values if no data exists yet
        exercise_frequency = 0
        diet_quality = 0
        sleep_hours = 0

    return render(request, 'profile.html', {'symptoms': symptoms, 
                                            'appointments': appointments, 
                                            'upcoming_appointments': upcoming_appointments, 
                                            'exercise_frequency_data': exercise_frequency,
                                            'diet_quality_data': diet_quality, 
                                            'sleep_hours_data': sleep_hours,
                                            })




@login_required
def update_profile_data(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.gender = request.POST.get('gender')
        profile.weight = request.POST.get('weight')
        profile.age = request.POST.get('age')
        profile.save()
        return redirect('profile')  # Redirect to the dashboard or relevant page

    return render(request, 'profile.html')



@login_required
def update_profile_data(request):
    if request.method == 'POST':
        # Retrieve the data from the POST request
        exercise_frequency = request.POST.get('exercise_frequency')
        diet_quality = request.POST.get('diet_quality')
        sleep_hours = request.POST.get('sleep_hours')
        appointment_feedback = request.POST.get('appointment_feedback')

        # Remove the first record for the user (oldest data)
        updateData.objects.filter(user=request.user).first().delete()
        
        # Save the data in the database
        health_data = updateData.objects.create(
            user=request.user,
            exercise_frequency=exercise_frequency,
            diet_quality=diet_quality,
            sleep_hours=sleep_hours,
            appointment_feedback=appointment_feedback,
        )
        
        return redirect('profile')  # Redirect to the profile after saving the data
    
    return render(request, 'update_profile_data.html')


from django.db.models import Count

@login_required
def profile_view(request):
    # Fetch the user's update data (you can filter by user if necessary)
    health_data = updateData.objects.filter(user=request.user)

    # Aggregate data for charts
    exercise_frequency_data = health_data.values('created_at__date').annotate(Count('exercise_frequency'))
    diet_quality_data = health_data.values('diet_quality').annotate(Count('diet_quality'))
    sleep_hours_data = health_data.values('created_at__date').annotate(Count('sleep_hours'))
    appointment_feedback_data = health_data.values('appointment_feedback').annotate(Count('appointment_feedback'))

    # Prepare data for charts
    exercise_dates = [entry['created_at__date'] for entry in exercise_frequency_data]
    exercise_frequencies = [entry['exercise_frequency__count'] for entry in exercise_frequency_data]

    diet_quality_values = [entry['diet_quality'] for entry in diet_quality_data]
    diet_quality_counts = [entry['diet_quality__count'] for entry in diet_quality_data]

    sleep_dates = [entry['created_at__date'] for entry in sleep_hours_data]
    sleep_hours = [entry['sleep_hours__count'] for entry in sleep_hours_data]

    appointment_feedback_values = [entry['appointment_feedback'] for entry in appointment_feedback_data]
    appointment_feedback_counts = [entry['appointment_feedback__count'] for entry in appointment_feedback_data]

    # Retrieve the latest entry for name, phone, address, gender, weight, and age
    latest_data = health_data.last()


    # Pass the data to the template
    context = {
        'exercise_dates': exercise_dates,
        'exercise_frequencies': exercise_frequencies,
        'diet_quality_values': diet_quality_values,
        'diet_quality_counts': diet_quality_counts,
        'sleep_dates': sleep_dates,
        'sleep_hours': sleep_hours,
        'appointment_feedback_values': appointment_feedback_values,
        'appointment_feedback_counts': appointment_feedback_counts,
    }

    return render(request, 'profile.html', context)


from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the form data into the Contact model
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

        # Return a success message as a JSON response
        return JsonResponse({'message': 'Your request has been submitted successfully!'})

    return render(request, 'contact.html')

from .models import UserProfile
@login_required
def update_basic_details(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        age = request.POST.get('age')

        # Assuming these additional fields are stored in a UserProfile model linked to the User model
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.phone = phone
        user_profile.address = address
        user_profile.gender = gender
        user_profile.weight = weight
        user_profile.age = age
        user_profile.save()

        return redirect('profile')  # Redirect back to profile page after updating

    return render(request, 'profile.html')