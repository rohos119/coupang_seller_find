window.addEventListener('DOMContentLoaded', function()
{
    // func();
    				var section = document.getElementById('dbinput');
                    var requestURL = "http://202.182.109.215/api/mancatdb/json";
                    var request = new XMLHttpRequest();
                    request.open('GET', requestURL);
                    request.responseType ='json';
                    request.send();

                    request.onload = function () {
						alert("Loading completed")
						var productData = request.response;
						showDatainfo(productData[productData.length-1]);
						showData(productData);

						function showData(jsonObj) {
							for (var i = 0; i < jsonObj.length; i++) {
								var row = section.insertRow(section.rows.length);
								var cell0 = row.insertCell(0); var cell1 = row.insertCell(1);
								var cell2 = row.insertCell(2); var cell3 = row.insertCell(3);
								var cell4 = row.insertCell(4); var cell5 = row.insertCell(5);
								// var cell6 = row.insertCell(6); var cell7 = row.insertCell(7);

								var checkbox = document.createElement('input');
								checkbox.setAttribute('type', 'checkbox');
								checkbox.setAttribute('class', 'user_CheckBox');
								cell0.appendChild(checkbox)

								var link = document.createElement('a');
								link.innerHTML = jsonObj[i].catname;
								link.setAttribute("id", "title-link")
								link.setAttribute("href", "https://www.coupang.com/np/categories/" + jsonObj[i].catnum)
								link.setAttribute('target', "_blank")

								cell1.appendChild(link); cell2.innerHTML = jsonObj[i].catnum;
								cell3.innerHTML = jsonObj[i].update;
								if(jsonObj[i].crawl_update != '0') cell4.innerHTML = jsonObj[i].crawl_update; else cell4.innerHTML="-";
								if(jsonObj[i].crawl_update != '0') cell5.innerHTML = "성공"; else cell5.innerHTML ="실패";

							}
						}

						function showDatainfo(jsonObj) {
							var infoinput = document.getElementsByClassName("table-responsive")[0];
							var cat_len = document.createElement('li');
							var cat_setting = document.createElement('li');
							var update = document.createElement('li');
							// setting 파일에서 가져오기
							var settinginfo = "카테고리 색인 설정 : ";
							if(jsonObj[0].sorter ='latestAsc') settinginfo += '최신순 /';
							settinginfo += "별점" + jsonObj[0].rating +"개 이상 / " + "도착예정일+" + jsonObj[0].delivery + "일 이상"
							cat_setting.innerHTML = settinginfo
							infoinput.prepend(cat_setting);

							//차후수정 jsonObj.length -1
							cat_len.innerHTML = "남자 카테고리DB 수 : " + productData.length;
							infoinput.prepend(cat_len);

							//update 일자
							update.innerHTML = "최신 업데이트 완료 시간 : " + productData[0].crawl_update;
							infoinput.prepend(update);

						}

						var table = $('#dataTable').DataTable( {});
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
								// $.ajax({
      							// 	url:"/login/mancatdb",
      							// 	type:"POST",
      							// 	data:JSON.stringify(aJsonArray),
      							// 	contentType: "application/json",
      							// 	success: function(result) {
          						// 	if (result) {
            					//   		alert("저장되었습니다.");
          						// 	} else {
           	 					//   		alert("잠시 후에 시도해주세요.");
          						// 	}
      							// 	},error: function() {
          						// 			alert("에러 발생");
      							// 	}
								// })
								console.log(aJsonArray);
						}

						btninput.append(selectall);
						btninput.append(deletebtn);
					}


});


