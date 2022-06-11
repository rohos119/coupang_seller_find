window.addEventListener('DOMContentLoaded', function()
{
    // func();
    // 				var section = document.getElementById('dbinput');
    //                 var requestURL = "http://127.0.0.1:8000/api/productdb/json";
    //                 var request = new XMLHttpRequest();
    //                 request.open('GET', requestURL);
    //                 request.responseType ='json';
    //                 request.send();

                    // request.onload = function () {
	alert("Loading completed")
	// var productData = request.response;
	// showDatainfo(productData[productData.length-1]);
	//showData(productData);

						// function showData(jsonObj) {
						// 	for (var i = 0; i < jsonObj.length-1; i++) {
						//
						// 		var row = section.insertRow(section.rows.length);
						// 		var cell0 = row.insertCell(0); var cell1 = row.insertCell(1);
						// 		var cell2 = row.insertCell(2); var cell3 = row.insertCell(3);
						// 		var cell4 = row.insertCell(4); var cell5 = row.insertCell(5);
						// 		var cell6 = row.insertCell(6); var cell7 = row.insertCell(7);
						//
						// 		var checkbox = document.createElement('input');
						// 		checkbox.setAttribute('type', 'checkbox');
						// 		checkbox.setAttribute('name', 'user_CheckBox');
						// 		cell0.appendChild(checkbox);
						//
						// 		var link = document.createElement('a');
						// 		link.innerHTML = jsonObj[i].title;
						// 		link.setAttribute("id", "title-link");
						// 		link.setAttribute("href", "https://www.coupang.com/vp/products/" + jsonObj[i].productid + "?vendorItemId=" + jsonObj[i].vendorid);
						// 		link.setAttribute('target', "_blank");
						//
						// 		cell1.innerHTML = jsonObj[i].seller_name;
						// 		cell2.appendChild(link); cell3.innerHTML = jsonObj[i].disc_price;
						// 		cell4.innerHTML = jsonObj[i].ven_productcd; cell5.innerHTML = jsonObj[i].productid;
						// 		cell6.innerHTML = jsonObj[i].vendorid; cell7.innerHTML = jsonObj[i].update;
						//
						// 	}
						// }

						// function showDatainfo(jsonObj) {
						// 	var total_prd=0;
						// 	var total_ven=0;
						// 	var infoinput = document.getElementsByClassName("table-responsive")[0];
						//
						// 	//상품별DB수
						// 	for ( var i=0; i < jsonObj.length; i++) {
    					// 		var datainfo = document.createElement('li');
    					// 		datainfo.setAttribute('class', 'datainfo');
    					// 		datainfo.style.float ="left"; datainfo.style.marginLeft = "10px";
    					// 		datainfo.innerHTML = "<a href='#'>" + jsonObj[i]._id + "</a>"
						// 		                    + " <span> ( "+jsonObj[i].tot_prd+" / "+jsonObj[i].tot_ven+" ) </span>";
    					// 		infoinput.prepend(datainfo);
    					// 		total_prd+= jsonObj[i].tot_prd
    					// 		total_ven+= jsonObj[i].tot_ven
						//
						// 	}
						// 	//전체상품DB수
						// 	var total = document.createElement('li');
						// 	total.setAttribute('class', 'totalinfo'); total.style.float="left";
						// 	total.innerHTML = "<a href='#'>전체</a>"
						// 		              + " <span> ( "+total_prd+" / "+total_ven+" ) </span>";
						// 	infoinput.prepend(total);
						// 	//설명부분
						// 	var explain = document.createElement('li');
						// 	explain.innerHTML ="상품DB ( 노출상품ID / 옵션ID )";
						// 	infoinput.prepend(explain);
						//
						// 	//최근업데이트
						// 	var updatelog = document.createElement('li');
						// 	updatelog.innerHTML="최근업데이트 : " + productData[productData.length-2].update;
						// 	infoinput.prepend(updatelog);
						// }

	var table = $('#dataTable').DataTable({});
	var liinfo = document.getElementsByClassName("table-responsive")[0];
	var datawrap = document.getElementsByClassName("dataTables_wrapper")[0];
	datawrap.style.marginTop='15px';
	var btninput = document.getElementsByClassName("dataTables_length")[0];
	btninput.firstElementChild.style.marginLeft='5px';
	btninput.style.display ='inline-block';
	var selectall = document.createElement('button'); selectall.innerHTML = '전체선택';
	var deletebtn = document.createElement('button'); deletebtn.innerHTML = '삭제';
	var showbtn = document.createElement('button'); showbtn.innerHTML = '모두펼처보기';
	selectall.setAttribute('id','selectBtn');
	deletebtn.setAttribute('id','deleteBtn');
	showbtn.setAttribute('id','showbtn');
	selectall.style.float = 'left';
	deletebtn.style.float = 'left'; deletebtn.style.marginLeft = '5px';
	showbtn.style.float = 'left'; showbtn.style.marginLeft = '5px';
	btninput.append(selectall);
	btninput.append(deletebtn);
	// btninput.append(showbtn);
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
			console.log(aJson);
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

	//}
	showbtn.onclick = function () {
		showrow = document.getElementsByClassName("win")
		for(var i=0;i<showrow.length;i++){
			if(showrow[i].style.display == 'none')
				showrow[i].style.display ="table-row";
			else
				showrow[i].style.display ="none";

		}
	}
});




