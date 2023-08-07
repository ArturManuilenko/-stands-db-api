function showMessage(data) {
    //alert(data['data']);
}

function setProgress(id, value) {
    var progress = document.getElementById(id);
    progress.setAttribute('value', value);
}

function waitResult(id, progress_id, url, params) {
    if (params == null) params = {}
    function answer(data) {        
        if (data.ready) {
            var progress = document.getElementById(progress_id);
            progress.style.display = 'none';
            params['id'] = id
            $("#result").load(url, params);
        } else {
            setProgress(progress_id, data.value);
            jQuery.getJSON('json_handler.py', { "cmd": "progress", "id": id }, answer);
        }
    }
    jQuery.getJSON('json_handler.py', { "cmd": "progress", "id": id }, answer);
}

function waitFile(id, progress_id, link_id, doctype=1) {
    function answer(data) {        
        if (data.ready) {
            var progress = document.getElementById(progress_id);
            progress.style.display = 'none';
            if(link_id){
            	var a = document.getElementById(link_id);
            	a.href = 'download.py?cmdid=' + id;
            	a.innerHTML = 'Если скачивание не началось нажмите эту на ссылку';
            }
            location.replace('download.py?doc=' + doctype + '&cmdid=' + id);
        } else {
            setProgress(progress_id, data.value);
            jQuery.getJSON('json_handler.py', { "cmd": "progress", "id": id }, answer);
        }
    }
    jQuery.getJSON('json_handler.py', { "cmd": "progress", "id": id }, answer);
}

function waitResultTable(id, progress_id, params) {
    waitResult(id, progress_id, "result_table.py", params);
}

function keepResult(id) {
    function answer(data) {
    }
    jQuery.getJSON('json_handler.py', { "cmd": "keep", "id": id }, answer);
}

//jQuery.getJSON('ajax_handler.py', { 'data': 'dara' }, showMessage);