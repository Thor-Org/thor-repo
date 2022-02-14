Python command:
<?php
$command1 = escapeshellcmd("python3 encryptUserFile.py test.txt");
$output = shell_exec($command1);
echo "<br>Combo: ";
echo $output;
?>


<?php
$servername = "192.168.1.5";
$username = "root";
$password = "Sadie1289";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
  die("Server: Connection failed: " . $conn->connect_error);
}
echo "Server: Connected<br>";
?>

<?php
          if(isset($_POST['button1'])) {
              $sql = "SELECT * FROM Lightning_Data.combinations
                      ORDER BY RAND()
                      LIMIT 1";
              $result = $conn->query($sql);

              if ($result->num_rows > 0) {
                // output data of each row
                while($row = $result->fetch_assoc()) {
                  $combination = $row["combination"];
                  $strike_time = $row["strike_time"];
                  $nano_seconds = $row["nano_seconds"];
                  $lat = $row["lat"];
                  $lon =$row["lon"];
                  $rise = $row["rise_time"];
                  $fall = $row["fall"];
                  $peak = $row["peak_cur"];
                  //$tex = "Key: ";
                  //echo "Strike time: $strike_time lat: $lat lon: $lon ";
                  //echo $lon;
                  // echo "strike_time: " . $row["strike_time"]. " - lat: " . $row["lat"]. " - lon: " . $row["lon"]. "<br>";
                  // echo "strike_time: " . $strike_time. " - lat: " . $lat. " - lon: " . $lon. "<br>";
                }
                $result->free();
              } else {
                echo "0 results";
              }

              $sql2 = "SELECT * FROM Lightning_Data.keys
                      ORDER BY RAND()
                      LIMIT 1";
              $result2 = $conn->query($sql2);

              if ($result2->num_rows > 0) {
                // output data of each row
                while($row2 = $result2->fetch_assoc()) {
                  $key =$row2["key"];
                }
                $result2->free();
              } else {
                echo "0 keys";
              }

          }
          if(isset($_POST['button2'])) {
            // echo "This is Button2 that is selected with" .$strike_time.;
            echo $strike_time;
            echo $lat;
            echo $lon;
        }
      ?>
