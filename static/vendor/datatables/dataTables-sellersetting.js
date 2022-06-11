window.addEventListener('DOMContentLoaded', function()
{

	$('#selectall').click(function(){
		var cbs = document.getElementsByTagName('input');
		for(var i=0; i < cbs.length; i++) {
			if(cbs[i].checked == false) {
				cbs[i].checked = true;
			}else{
				cbs[i].checked = false;
			}
		}
	});
	$('#deletebtn').click(function(){
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
			aJson.seller_name = td.eq(2).text();
			aJsonArray.push(aJson);
		});
		console.log(aJsonArray)
		alert(aJsonArray.length+"셀러 설정을 변경하시겠습니까?")
		$.ajax({
			url:"",
			type:"POST",
			data:JSON.stringify(aJsonArray),
			contentType: "json",
			success: function(result) {
				if (result) {
					alert("매칭셀러로 변경 되었습니다.");
				} else {
					alert("잠시 후에 시도해주세요.");
				}
				},error: function() {
				alert("에러 발생");
			}
		})
	});

});


