from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def career():
    return render_template("hometest.html")

@app.route('/predict', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form.to_dict(flat=True)  # Convert form data to dictionary
        print("Form Data:", result)
        
        # Convert form values to a numeric array
        try:
            arr = [float(value) for value in result.values()]  # Convert strings to float
        except ValueError:
            return "Error: Please enter valid numeric inputs."

        data = np.array(arr).reshape(1, -1)  # Reshape to match model input
        print("Processed Input:", data)

        # Load the trained model
        loaded_model = pickle.load(open("careerlast.pkl", 'rb'))

        # Make predictions
        predictions = loaded_model.predict(data)
        print("Predicted Job Index:", predictions)

        pred_proba = loaded_model.predict_proba(data)
        print("Prediction Probabilities:", pred_proba)

        # Threshold filtering
        pred_filtered = pred_proba > 0.05

        # Get recommended job indices
        recommended_jobs = [i for i in range(17) if pred_filtered[0, i]]
        recommended_jobs = [job for job in recommended_jobs if job != predictions[0]]  # Remove top prediction

        # Job dictionary
        jobs_dict = {
            0: 'AI ML Specialist', 1: 'API Integration Specialist', 2: 'Application Support Engineer',
            3: 'Business Analyst', 4: 'Customer Service Executive', 5: 'Cyber Security Specialist',
            6: 'Data Scientist', 7: 'Database Administrator', 8: 'Graphics Designer',
            9: 'Hardware Engineer', 10: 'Helpdesk Engineer', 11: 'Information Security Specialist',
            12: 'Networking Engineer', 13: 'Project Manager', 14: 'Software Developer',
            15: 'Software Tester', 16: 'Technical Writer'
        }

        predicted_job = jobs_dict.get(predictions[0], "Unknown Job")  # Get predicted job name
        recommended_job_names = [jobs_dict.get(job, "Unknown Job") for job in recommended_jobs]  # Get job names

        return render_template("testafter.html", final_res=recommended_job_names, job0=predicted_job)

if __name__ == '__main__':
    app.run(debug=True)
