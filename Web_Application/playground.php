Python command:
<?php
$command1 = escapeshellcmd("python3 MD5Hash.py 1");
$output = shell_exec($command1);
echo "<br>Hash: ";
echo $output;
?>
