var new_card_id = 0;

function set_new_card(key, info)
{
  document.getElementById("add_card_info").innerHTML = "<img src=\"/icons/card.png\" height=24>" + key;
  document.getElementById("add_card_label").innerHTML = info;
  new_card_id = key;
  edit_change(document.getElementById("add_card"));
}

function rfid_ready(data) {
    if(data["error"]){
        alert("ОШИБКА: " + data["error"]);
        window.location.reload(true);
    } 
    if(data["info"].length == 0){
        send_rfid_request();
    }else{
      set_new_card(data["key"], data["info"]);
    }
};

function send_rfid_request() {
    if(new_card_id==0) $.ajax({
      method: "POST",
      url: "json_handler.py",
      data: { cmd: "last_rfid" }
    })
      .done(rfid_ready);
};


function start_card_search(){
  var row = document.getElementById("add_card");
  send_rfid_request();
  edit_show(row);
  var row_man = document.getElementById("add_card_man");
  if(row_man){
    row_man.style.display = "none";
  }
}

function stard_add_card_man(elem)
{
  edit_show(elem);
  var row = document.getElementById("add_card");
  if(row){
    row.style.display = "none";
  }
}

function card_man_hex_change(elem)
{
  var text = document.getElementById("hex_card_man").value
  if(text.length==10){
    document.getElementById("card_man").value = parseInt(text, 16);
    edit_change(elem);
  }
  else if(text.length==16){
    document.getElementById("card_man").value = parseInt(text.substring(4,14), 16);
    edit_change(elem);
  }
  else{
    document.getElementById("card_man").value = '';
  }
}

function card_man_change(elem)
{
  document.getElementById("hex_card_man").value = "";
  edit_change(elem);
}

function apply_new_card_man(user_id)
{
  new_card_id = document.getElementById("card_man").value;
  $.ajax({
    method: "POST",
    url: "json_handler.py",
    data: {cmd: "card_info", id: new_card_id}
  })
    .done(function(data) {
      if(data["error"]){
          alert("ОШИБКА: " + data["error"]);
          window.location.reload(true);
      }
      else{
        if(data["new"] == 0 && !confirm(data["info"] + "\nВы уверены, что хотите передать карту текущему пользователю?")){
          window.location.reload(true);
        }
        else{
          apply_new_card(user_id);
        }
      }
                
    });
}

function apply_new_card(user_id)
{
  $.ajax({
    method: "POST",
    url: "json_handler.py",
    data: {cmd: "modify_card", id: new_card_id, user: user_id, enabled: 1}
  })
    .done(function(data) {
      if(data["error"]){
          alert("ОШИБКА: " + data["error"]);
      }      
      window.location.reload(true);          
    });
}

function create_user()
{
  var name_f = document.getElementById("name_f").value;
  var name_i = document.getElementById("name_i").value;
  var name_o = document.getElementById("name_o").value;
  $.ajax({
    method: "POST",
    url: "json_handler.py",
    data: {cmd: "create_user", f: name_f, i: name_i, o: name_o}
  })
    .done(function(data) {
      if(data["error"]){
          alert("ОШИБКА: " + data["error"]);
      }      
      else{
        location.href='/cgi_bin/edituser.py?id=' + data["id"];
      }        
    });
}