function ref_code(obj){
    obj.src = obj.src;
}
function getCookie(c_name)
{
if (document.cookie.length>0)
  {
  c_start=document.cookie.indexOf(c_name + "=")
  if (c_start!=-1)
    { 
    c_start=c_start + c_name.length+1 
    c_end=document.cookie.indexOf(";",c_start)
    if (c_end==-1) c_end=document.cookie.length
    return unescape(document.cookie.substring(c_start,c_end))
    } 
  }
return ""
}
function smt_func(){
    var authcode = getCookie("yunzlog_authcode");
    var inputcode = $("#cmt_code").val();
    if(authcode.toLowerCase()==inputcode.toLowerCase()){
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
          $("#cmt_author").html($("#name").val());
          $("#cmt_ctt").html($("#cmtext").val());
          //need change date
          $("#comments-list").prepend($("#cmt_ajax").html());
          $('#cmt_form')[0].reset();
        },
      });
    }else{
      alert("auth code error!authcode="+authcode);
      $('#cmt_code').val("");
      var obj = $("#smt_img"); 
      ref_code(obj);
    }
    return false;
}