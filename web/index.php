<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="style.css">
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
<title>WiFi-Mapper</title>
</head>
<style>
	#output {padding-left: 10px}
</style>
<body>
<?php
$connected = False;
$path_db = ''; # Change to the path of the .db file
if (file_exists($path_db)) {
	$db = new SQLite3($path_db);
	$connected = True;
}
?>

<p id='conn_info' class='controls'>Connecting to DB...</p>
<script type='text/javascript'>
	var is_conn = <?php if ($connected) {print 1;} else {print 0;} ?>;
	var conn_db = 'Connected to DB!';
	var no_conn_db = 'Not connected to DB!';
	if (is_conn) {
		document.getElementById('conn_info').innerHTML = conn_db.fontcolor('green');
	} else {
		document.getElementById('conn_info').innerHTML = no_conn_db.fontcolor('red');
	}
</script>

<?php
if ($connected) {
	$res = $db->query('SELECT * FROM [MAPPER DATA]');
	print "<form class='controls' action='#' method='post'>";
	print "<select name='SSID_select[]' id='SSID_select'>";
	while ($row = $res->fetchArray()) {
		print "<option value='{$row["ID"]}'>{$row['ID']}</option>";
	}
	print "</select>";
	print "<input type='submit' name='submit' value='Get Info' />";
	print "</form>";
	if (isset($_POST['submit'])) {
		print "<div class='info_list'>";
		foreach ($_POST['SSID_select'] as $id) {
			while ($row = $res->fetchArray()) {
				$coords = "{$row['LATITUDE']},{$row['LONGITUDE']}";
				if ($row['ID'] == $id) {
					print "
					<h3>{$row['ID']} - {$row['SSID']}</h3>
					<p>MACADDR:{$row['MAC']}</p>
					<p>QS:{$row['QUAL / SIGN']}</p>
					<p>CHANNEL:{$row['CHANNEL']}</p>
					<p>ENCRYPT:{$row['ENCRYPTED']}</p>
					<p>DIST:{$row['DISTANCE']}</p>
					<p>LAT/LON:{$row['LATITUDE']},{$row['LONGITUDE']}</p>
					<p>LOC: {$row['LOCATION']}</p>";
				}
			}
		}
		print "</div>";
	}
	print "<iframe
		id='map'
		width='420'
		height='420'
		src='https://maps.google.com/maps?q={$coords}&t=k&z=13&ie=UTF8&iwloc=&output=embed'></iframe>";
}
?>
<style>
	#output {padding-left: 10px}
</style>
</body>
</html>
