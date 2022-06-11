window.addEventListener('DOMContentLoaded', function()
{
    // func();

						var datawrap = document.getElementsByClassName("dataTables_wrapper")[0];
						datawrap.style.marginTop='15px';
						var btninput = document.getElementsByClassName("dataTables_length")[0];
						btninput.firstElementChild.style.marginLeft='5px'
						var selectall = document.createElement('button'); selectall.innerHTML = '전체선택';
						var deletebtn = document.createElement('button'); deletebtn.innerHTML = '삭제';
						selectall.setAttribute('id','selectBtn'); deletebtn.setAttribute('id','deleteBtn');
						selectall.style.float = 'left'; deletebtn.style.float = 'left'; deletebtn.style.marginLeft = '5px';
						selectall.onclick = function(){
							var cbs = document.getElementsByTagName('input');
                    			for(var i=0; i < cbs.length; i++) {
                        			if(cbs[i].checked == false) {
                            			cbs[i].checked = true;
                        			}else{
                        				cbs[i].checked = false;
									}
                    			}
							};

						deletebtn.onclick = function(){
								var tdArr = new Array();
								var checkbox = $("input[class=user_CheckBox]:checked");
								var aJsonArray = new Array();
								// 체크된 체크박스 값을 가져온다
								checkbox.each(function(i) {
								// checkbox.parent() : checkbox의 부모는 <td>이다.
								// checkbox.parent().parent() : <td>의 부모이므로 <tr>이다.
									var tr = checkbox.parent().parent().eq(i);
									var td = tr.children();
									var aJson = new Object();
									aJson.catname = td.eq(1).text();
									aJson.catnum = td.eq(2).text();
									aJsonArray.push(aJson);
								});
								alert(aJsonArray.length+"개의 카테고리를 삭제하시겠습니까?")
								$.ajax({
      								url:"",
      								type:"POST",
      								data:JSON.stringify(aJsonArray),
      								contentType: "json",
      								success: function(result) {
          							if (result) {
            					  		alert("삭제되었습니다.");
          							} else {
           	 					  		alert("잠시 후에 시도해주세요.");
          							}
      								},error: function() {
          									alert("에러 발생");
      								}
								})
						}
						btninput.append(selectall);
						btninput.append(deletebtn);


});


