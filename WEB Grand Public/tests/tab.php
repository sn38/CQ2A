<?php

$sql = "SELECT date,value FROM temperature where  date &gt; (NOW() - INTERVAL 24 HOUR)";
$result = $conn->query($sql);
 
 
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $data[] = $row['value'];
        $data_label[] = $row['date'];
    }
} else {
    echo "0 results";
}
 
$sql2 = "SELECT cast(avg(value) AS DECIMAL(10,2)) as avg FROM temperature where date > (NOW() - INTERVAL 24 HOUR)";
$result2 = $conn->query($sql2);
$row = $result2->fetch_assoc();
for($i=0;$i<count($data);$i++){
    $moyenne[$i] = $row;
}