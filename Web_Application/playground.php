Python command:
<?php
$command1 = escapeshellcmd("python3 encryptUserFile.py test.txt");
$output = shell_exec($command1);
echo "<br>Combo: ";
echo $output;
?>

<?php
   if(isset($_FILES['image'])){
      $errors= array();
      $file_name = $_FILES['image']['name'];
      $file_size = $_FILES['image']['size'];
      $file_tmp = $_FILES['image']['tmp_name'];
      $file_type = $_FILES['image']['type'];
      $file_ext=strtolower(end(explode('.',$_FILES['image']['name'])));

      $extensions= array("jpeg","jpg","png","txt");

      if(in_array($file_ext,$extensions)=== false){
         $errors[]="extension not allowed, please choose a JPEG, PNG or TXT file.";
      }

      if($file_size > 2097152) {
         $errors[]='File size must be exactly 2 MB';
      }

      if(empty($errors)==true) {
         move_uploaded_file($file_tmp,"uploads/".$file_name);
         echo "Success";

          $command3 = escapeshellcmd("python3 encryptUserFile.py $file_name");
          $output = shell_exec($command3);
          echo "<br>Combo: ";
          echo $output;
      }else{
         print_r($errors);
      }
   }
?>

<html>
   <body>

      <form action = "" method = "POST" enctype = "multipart/form-data">
         <input type = "file" name = "image" />
         <input value="button3" name="button3" type = "submit"/>

         <ul>
            <li>Sent file: <?php echo $_FILES['image']['name'];  ?>
            <li>File size: <?php echo $_FILES['image']['size'];  ?>
            <li>File type: <?php echo $_FILES['image']['type'] ?>
            <li>Encrypted File: <?php echo $_FILES['image']['name'] ?>_ENCRYPTED <a href="http://97.102.250.88/uploads/<?php echo $_FILES['image']['name'] ?>_ENCRYPTED"> Download Encrypted File</a>
            <li>Receipt: <?php echo $_FILES['image']['name'] ?>_RECEIPT <a href="http://97.102.250.88/uploads/<?php echo $_FILES['image']['name'] ?>_RECEIPT"> Download Receipt File</a>
         </ul>

      </form>

   </body>
</html>
