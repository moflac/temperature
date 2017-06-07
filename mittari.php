<?php setlocale(LC_ALL, 'fi_FI');
 $lastmod = date("H:i:s d-m-Y", filemtime("temperature/temp_daily.png")); ?>
<html>
<head>
  <meta http-equiv="cache-control" content="no-cache">
  <meta http-equiv="refresh" content="3600" >
  <title>Raspimittari</title>
  <style>
      BODY
      {
        font-family: arial;
        font-size: 10pt;
        background-repeat: no-repeat; background-position: center center;
      }
 
      H2, H3 { margin-bottom: 0; }
  </style>
</head>
<body>
  <div style="width: 800px; margin-left: 100px;" >
    <h2>L�mp�tila sis�ll� (Ahvena) ja ulkona (Pirkkala lentokentt�)</h2>
    <i>Viimeksi p�ivitetty: <?=$lastmod?></i>
    
	<h3>Tunti</h3>
    <img src="temperature/temp_hourly.png" />
	
    <h3>P�iv�</h3>
    <img src="temperature/temp_daily.png" />
     
    <h3>Viikko</h3>
    <img src="temperature/temp_weekly.png" />
     
    <h3>Kuukausi</h3>
    <img src="temperature/temp_monthly.png" />
     
    <h3>Vuosi</h3>
    <img src="temperature/temp_yearly.png" />
  </div>
</body>
</html>

