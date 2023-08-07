function stendCheckAll(name, value) {
    var elems = document.getElementsByName(name);
    for (var i = 0; i < elems.length; ++i) {
        elems[i].checked = value;
    }
}

function stendUserChecked(elem){
    if(elem.checked == false){
        let stend = parseInt(elem.value);
        var group_list = [];
        for(var i = 0; i < stend_group_binds.length; ++i){
            if(stend_group_binds[i][0] == stend) group_list.push(stend_group_binds[i][1]);
        }

        var groups = document.getElementsByClassName("stend-group-check");
        for (var i = 0; i < groups.length; ++i) {
            if(group_list.includes(parseInt(groups[i].value))){
                groups[i].checked = false;
            }
        }
    }
}

function groupUserChecked(elem){
    let group = parseInt(elem.value);

    var stend_list = [];
    for(var i = 0; i < stend_group_binds.length; ++i){
        if(stend_group_binds[i][1] == group) stend_list.push(stend_group_binds[i][0]);
    }

    var stends = document.getElementsByName("st");
    for (var i = 0; i < stends.length; ++i) {
        if(stend_list.includes(parseInt(stends[i].value))){
            stends[i].checked = elem.checked;
        }
    }
}