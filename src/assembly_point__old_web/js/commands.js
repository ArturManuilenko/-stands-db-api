function send_command(cmddata)
{
	$.ajax({
	      method: "POST",
	      url: "json_handler.py",
	      data: cmddata
	    })
	      .done(function(data) {
	        if(data["error"]){
	            alert("ОШИБКА: " + data["error"]);
	        } 
	        window.location.reload(true);
	      });
}

function delMod(id) {
	var cnf = confirm("Вы уверены, что хотите удалить модификацию?");
	if(cnf){
		$.ajax({
	      method: "POST",
	      url: "json_handler.py",
	      data: {cmd: "del_mod", id: id}
	    })
	      .done(function(data) {
	        if(data["error"]){
	            alert("ОШИБКА: " + data["error"]);
	        } 
	        window.location.reload(true);
	      });
  	}
}

function lockUser(id) {
	send_command({cmd: "modify_user", id: id, enabled: 0});
}

function unlockUser(id) {
	send_command({cmd: "modify_user", id: id, enabled: 1});
}

function lockGroup(id) {
	send_command({cmd: "modify_group", id: id, enabled: 0});
}

function unlockGroup(id) {
	send_command({cmd: "modify_group", id: id, enabled: 1});
}
