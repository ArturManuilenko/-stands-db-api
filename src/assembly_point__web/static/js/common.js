if ($.cookie("devices_sort_by") == null && $.cookie("devices_sort_direction") == null) {
    $.cookie("devices_sort_by", "date_modified", {secure: true, expires: 7});
    $.cookie("devices_sort_direction", "desc", {secure: true, expires: 7});
    $(".devices_sort_by option[value=date_modified-desc]").prop('selected', true);
} else if ($.cookie("devices_sort_by") == null && $.cookie("devices_sort_direction") != null) {
    $.cookie("devices_sort_by", "date_modified", {secure: true, expires: 7});
    $(".devices_sort_by option[value=date_modified-" + $.cookie("devices_sort_direction") + "]").prop('selected', true);
} else if ($.cookie("devices_sort_by") != null && $.cookie("devices_sort_direction") == null) {
    $.cookie("devices_sort_direction", "desc", {secure: true, expires: 7});
    $(".devices_sort_by option[value=" + $.cookie("devices_sort_by") + "-desc]").prop('selected', true);
} else {
    var selector = ".devices_sort_by option[value=" + $.cookie("devices_sort_by") + "-" + $.cookie("devices_sort_direction") + "]";
    $(selector).prop('selected', true);
}

$(".devices_sort_by").prop('disabled', false);

$(".devices_sort_by").change(function() {
    var sort_order_field = $('.devices_sort_by option:selected').val();
    var params = sort_order_field.split('-');
    $.cookie("devices_sort_by", params[0], {secure: true, expires: 7});
    $.cookie("devices_sort_direction", params[1], {secure: true, expires: 7});
    location.reload();
});
