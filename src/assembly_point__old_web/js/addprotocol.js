var algoritm_name = undefined;
var mac_count = 0;

function add_mac(node)
{
  let mac_address = '';
  let inputs = node.parentNode.getElementsByTagName("input");
	for (let i = 0; i < inputs.length; ++i) {
		mac_address =  inputs[i].value;
    inputs[i].value = '';
	}
  $.ajax({
    method: "POST",
    url: "json_handler.py",
    data: {cmd: "protocol_device_info", mac: mac_address}
  })
    .done(function(data) {
      if(data["error"]){
          alert("ОШИБКА: " + data["error"]);
      }      
      else if(algoritm_name !== undefined && algoritm_name != data["algoritm"]){
        alert("ОШИБКА: неверный алгоритм поверки");
      }
      else{
        algoritm_name = data["algoritm"];

        let info_text = ' Прибор: ' + data['mac'] + ' от ' + data['datetime'];
        let report_id = data['report'];
        
        
        let div = document.createElement("div");        
        div.className = 'edit-row';
        div.innerHTML = `<div class="edit-info">Отчет</div><div class="edit-cell"><div class="edit-edit"><input type="text" readonly="readonly" name="report${mac_count}" value="${report_id}">${info_text}</div></div>`;
      
        let this_row = node.parentNode.parentNode.parentNode;
        this_row.parentNode.insertBefore(div, this_row);
        ++mac_count;
      }
    });
}