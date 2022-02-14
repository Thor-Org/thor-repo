Python command:
<?php
$command1 = escapeshellcmd("python3 encryptUserFile.py test.txt");
$output = shell_exec($command1);
echo implode("", $output);
echo "<br>Hash: ";
echo $output;
?>
