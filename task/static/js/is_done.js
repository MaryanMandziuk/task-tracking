function is_done(it) {
    var done = $(it).is(":checked") ? "1": "0";
    var id =  $(it).attr("id");
    var pos = id.lastIndexOf("-");
    id = id.slice(pos+1);
    $.ajax({
      type: 'GET',
      url: 'is_done/',
      data: {
        'id': id,
        'done': done,
      },
      dataType: 'json',
      success: function (data) {
          if(data["done"] == 1) {
              $('#'+'button-timer-'+id+' button').attr("disabled", true);
          } else {
              $('#'+'button-timer-'+id+' button').attr("disabled", false);
          }
      }
    });
};
