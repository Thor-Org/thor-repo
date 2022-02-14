Python command:
<?php

$command = 'python3 encryptUserFile.py test.txt';
# $command = 'ls';
exec($command, $output, $status);
echo $output[0];
echo var_dump($output)

?>
