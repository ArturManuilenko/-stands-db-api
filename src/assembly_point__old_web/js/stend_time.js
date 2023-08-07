function setStendTime(from, to) {
    jQuery.datetimepicker.setLocale('ru');
    jQuery('#datetimepicker_from').datetimepicker({
        format:'d.m.Y H:i',
        value: from,
    });
    jQuery('#datetimepicker_to').datetimepicker({
        format:'d.m.Y H:i',
        value: to,
    });
}