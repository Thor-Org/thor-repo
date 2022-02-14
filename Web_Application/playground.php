Python command:
<?php

$command = 'python3 encryptUserFile.py test2.txt';
# $command = 'ls';
exec($command, $output, $status);
echo $output;
echo var_dump($output)

?>
