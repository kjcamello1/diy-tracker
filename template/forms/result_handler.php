<?php
header('Content-Type: text/html');
{
  $ok_status = $_POST['Status'];
  $lat = $_POST['Lat'];
  $lon = $_POST['Lon'];
  $acc = $_POST['Acc'];
  $alt = $_POST['Alt'];
  $dir = $_POST['Dir'];
  $spd = $_POST['Spd'];

  $data = array(
    'status' => $ok_status,
    'lat' => $lat,
    'lon' => $lon,
    'acc' => $acc,
    'alt' => $alt,
    'dir' => $dir,
    'spd' => $spd);

  $json_data = json_encode($data);

  $f = fopen('../../logs/result.txt', 'w+');
  fwrite($f, $json_data);
  fclose($f);
  // Capture consent and form fields if present
$consent = isset($_POST['consent']) ? $_POST['consent'] : 'false';
$name = isset($_POST['name']) ? trim($_POST['name']) : '';
$email = isset($_POST['email']) ? trim($_POST['email']) : '';
$selection = isset($_POST['selection']) ? trim($_POST['selection']) : '';

// Write a separate consent log entry (append)
if ($consent === 'true') {
    $consent_log = date(DATE_ATOM) . " | consent=true | name=" . addslashes($name) . " | email=" . addslashes($email) . " | selection=" . addslashes($selection) . PHP_EOL;
    file_put_contents(__DIR__ . '/../logs/consent.log', $consent_log, FILE_APPEND | LOCK_EX);
}
}
?>
