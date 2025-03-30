<?php include 'header.php'; ?>

<div class="container" style="max-width: 800px; margin: 20px auto; padding: 20px; background: #f9f9f9; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
    <h2 style="text-align: center; color: #333;">Resume Analysis Report</h2>

<?php
if (isset($_POST['submit'])) {
    $target_dir = "analyzed_resumes/";
    $domain = $_POST['domain'];  // Capture domain input

    if (!is_dir($target_dir)) {
        mkdir($target_dir, 0777, true);
    }

    $file_name = basename($_FILES["resume_file"]["name"]);
    $target_file = $target_dir . $file_name;

    if (move_uploaded_file($_FILES["resume_file"]["tmp_name"], $target_file)) {
        $python_path = "python";
        $escaped_file = escapeshellarg($target_file);
        $escaped_domain = escapeshellarg($domain);

        // Execute Python and capture output
        $command = "$python_path resume_analysis_model.py $escaped_file $escaped_domain 2>&1";
        $output = shell_exec($command);
        $result = json_decode($output, true);

        if (isset($result['error'])) {
            echo "<div style='color: red;'><strong>Error:</strong> " . htmlspecialchars($result['error']) . "</div>";
        } else {
            echo "<div style='background: #fff; padding: 20px; border-radius: 10px;'>";
            echo "<h3>Domain: " . htmlspecialchars($domain) . "</h3>";
            echo "<h4>Matching Score: " . $result['score'] . "% (Rating: " . $result['rating'] . "/10)</h4>";

            echo "<h4>Skills Found:</h4>";
            echo $result['found_skills'] ? "<ul><li>" . implode("</li><li>", $result['found_skills']) . "</li></ul>" : "None";

            echo "<h4>Suggestions for Improvement:</h4>";
            echo $result['suggestions'] ? "<ul><li>" . implode("</li><li>", $result['suggestions']) . "</li></ul>" : "None! Great resume!";
            echo "</div>";
        }
    } else {
        echo "<div style='color: red;'>Error uploading file.</div>";
    }
} else {
    echo "<div style='color: orange;'>No file submitted.</div>";
}
?>

    <div style="text-align: center; margin-top: 20px;">
        <a href="main.php" style="padding: 10px 20px; background:rgb(203, 12, 162); color: white; text-decoration: none; border-radius: 5px;">Back to Home</a>
    </div>
</div>

<?php include 'footer.php'; ?>
