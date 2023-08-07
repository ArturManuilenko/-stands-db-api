function edit_add_value(data, node)
{
	var inputs = node.getElementsByTagName("input");
	for (var i = 0; i < inputs.length; ++i) {
		var input = inputs[i];
		if (input.type == "checkbox"){
			data[input.name] = input.checked ? 1 : 0;
		}
		else{
			data[input.name] = input.value;
		}
	}
	var selects = node.getElementsByTagName("select");
	for (var i = 0; i < selects.length; ++i) {
		var select = selects[i];
		data[select.name] = select.options[select.options.selectedIndex].value; 
	}
	return data;
}

function get_edit_cell(elem, classname = "edit-row")
{
	while (elem.className != classname){
		elem = elem.parentNode;
		if(elem == document) alert("Ошибка выполнения скрипта на сранице");
	}
	return elem;
}

function edit_show(elem)
{
	var row = get_edit_cell(elem, "edit-row")
	var edits = row.getElementsByClassName('edit-edit');
	for (var i = 0; i < edits.length; i++) {
		edits[i].style.display='flex';
	}
	var actions = row.getElementsByClassName('edit-actions');
	for (var i = 0; i < actions.length; i++) {
		actions[i].style.display='none';
	}
	var actions = row.getElementsByClassName('edit-show');
	for (var i = 0; i < actions.length; i++) {
		actions[i].style.display='none';
	}
	edit_change(elem);
}

function edit_show_actions(elem)
{
	var row = get_edit_cell(elem);
	var edits = row.getElementsByClassName('edit-edit');
	for (var i = 0; i < edits.length; i++) {
		edits[i].style.display='none';
	}
	var actions = row.getElementsByClassName('edit-actions');
	for (var i = 0; i < actions.length; i++) {
		actions[i].style.display='flex';
	}
}

function edit_change(elem)
{
	var row = get_edit_cell(elem);

	var btns = row.getElementsByTagName('button');
	for (var i = 0; i < btns.length; i++) {
		btns[i].style.display = btns[i].className == 'edit-confirm' ? 'inline' : 'none';
	}

	for (tag of ['input','select','button']){
		var inputs = document.getElementsByTagName(tag);
		for (var i = 0; i < inputs.length; i++) if(inputs[i] != elem) {				
			inputs[i].disabled = 'disabled';
		}
		var inputs = row.getElementsByTagName(tag);
		for (var i = 0; i < inputs.length; i++) if(inputs[i] != elem) {				
			inputs[i].disabled = null;
			inputs[i].onkeypress = null;
			inputs[i].onchange = null;
			inputs[i].oninput = null;
		}
	}

}

function edit_done(data)
{
	window.location.reload(true);
}

function edit_action(elem, command=null, add_values=true, done = edit_done)
{
	var row = get_edit_cell(elem);

	var btns = elem.parentNode.getElementsByTagName('button');
	for (var i = 0; i < btns.length; i++) {
		btns[i].style.display='none';
	}

	var inprogress = elem.parentNode.getElementsByClassName('edit-inprogress');
	for (var i = 0; i < inprogress.length; i++) {
		inprogress[i].style.display='inline';
	}

	for (tag of ['input','select']){
		var inputs = elem.parentNode.getElementsByTagName(tag);
		for (var i = 0; i < inputs.length; i++) {
			inputs[i].disabled='disabled';
		}
	}

	if(command){
		if(add_values) edit_add_value(command, row);
	    $.ajax({
	      method: "POST",
	      url: "json_handler.py",
	      data: command
	    })
	    .done(function(data) {
	        if(data["error"]){
	            alert("Ошибка: " + data["error"]);
	            window.location.reload(true);
	        }
	        else done(data);	        
	      })
	    .fail(function() {
	      	alert("Ошибка подключения при выполнении команды");
	      	window.location.reload(true);
	      });
	}
	else{
		window.location.reload(true);
	}	
}