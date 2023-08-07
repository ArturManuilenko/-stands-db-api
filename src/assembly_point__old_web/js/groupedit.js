function create_group()
{
  var name = document.getElementById("name").value;
  var description = document.getElementById("description").value;
  $.ajax({
    method: "POST",
    url: "json_handler.py",
    data: {cmd: "create_group", name: name, description: description}
  })
    .done(function(data) {
      if(data["error"]){
          alert("ОШИБКА: " + data["error"]);
      }      
      else{
        location.href='/cgi_bin/editgroup.py?id=' + data["id"];
      }        
    });
}