<?php include 'header.php'; ?>

<style>
    /* Full-page flex container */
    /* Centering the form in the viewport */
.page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f8f8f8;
}

/* Form container styling */
.form-container {
    max-width: 500px; /* Adjusted width */
    width: 90%;
    padding: 30px;
    background: linear-gradient(135deg, #ff69b4, #ff1493); /* Soft gradient */
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    text-align: center;
    color: white;
}

/* Form input and dropdown */
.form-container input,
.form-container select {
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    border: none;
    border-radius: 5px;
    background: white;
    color: black;
}

/* Buttons */
.btn {
    padding: 12px 20px;
    border: none;
    border-radius: 20px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s ease-in-out;
    display: block;
    width: 100%;
    margin: 10px 0;
}

.analyze-btn {
    background: #ff1493;
    color: white;
}

.back-btn {
    background: #ff4500;
    color: white;
    text-decoration: none;
}

.btn:hover {
    transform: scale(1.05);
}

</style>

<!-- Centered Page Container -->
<div class="page-container">
    <div class="form-container">
        <h2>Upload Your Resume for Analysis</h2>
        <form action="analyze_resume.php" method="POST" enctype="multipart/form-data">
            <input type="file" name="resume_file" accept=".pdf, .doc, .docx" required>
            <select name="domain" required>
                <option value="" disabled selected>Select Domain</option>
                <option>Application Support Engineer</option>
                <option>Graphics Designing</option>
                <option>Data Science</option>
                <option>Business Analysis</option>
                <option>Software Engineering</option>
                <option>AI ML</option>
                <option>Project Management</option>
                <option>Software Development</option>
                <option>Computer Networking</option>
                <option>Cyber Security</option>
                <option>Database Engineer</option>
            </select>
            <button type="submit" name="submit" class="btn analyze-btn">Analyze Resume</button>
        </form>
        <a href="main.php" class="btn back-btn">Back to Home</a>
    </div>
</div>

<?php include 'footer.php'; ?>
