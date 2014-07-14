function ref_code(obj){
    obj.src = obj.src;
}

function smt_func(){
    //var authcode = $.cookie("yunzlog_authcode",  { path: '/' });
    $.ajax({
      url: "/blog/comment",
      type: 'POST',
      data: {
        cmtext: $("#cmtext").val(),
        keyid: $("#keyid").val(),
        name: $("#name").val(),
        email: $("#email").val()
      },
      //get comment block and fill them with response data
      success: function(response) {
        $( response ).prependTo( "#comments-list" );
      },
    });
    return false;
}