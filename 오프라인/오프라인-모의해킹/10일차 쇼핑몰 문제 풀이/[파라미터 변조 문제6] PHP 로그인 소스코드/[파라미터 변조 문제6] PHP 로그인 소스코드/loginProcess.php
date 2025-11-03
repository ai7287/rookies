<?php header("Content-Type: text/html; charset=UTF-8");?>
<?php

	ini_set('display_errors', '0');

	include_once "../include/common/property.php";
	include_once "../include/common/class.db.php";
	include_once "../include/common/common.function.php";
	include_once "../include/common/JSON.php";
	include_once "../../request_log_exam48.php";

	include_once '../../aes/aes.class.php';
	include_once '../../aes/aesctr.class.php';

	$tName = "";
	$N_USER_ID		= charInChange(nvl(POST("login_id"), ''));
	$N_USER_PW	= nvl(AesCtr::decrypt(POST("login_pwd"),'incross',256), '');

	$resultDataArr = array();
	$json = new Services_JSON();

	$setParams					= array();
	$setParams['USER_ID']		= $N_USER_ID;
	$setParams['USER_PW']	= $N_USER_PW;


	if (strcmp(POST("login_id"),"answerxss@xss.com")==0&&strcmp(POST("login_pwd"),"Input_Random_PW")==0) {
		session_regenerate_id();
		session_start();
		$_SESSION['LOGIN_ID'] = 'answerxss@xss.com';
		$_SESSION['USER_NM'] = 'answer';

		$resultDataArr['result']		= "Y";	
	}else {
		$resultDataArr['result']			= "N";
	}


	$output = json_encode($resultDataArr);

	print( $output );

?>