//keep notify for new pic
$(document).ready(function() {
 var error_sleep_time = 500;
    function poll() {
        $.ajax({
            url: '/ajax',
            type: 'GET',
            success: function(result) {
		if (result=="new")
		    {
               // getnewpic();
			$("#notify").html("new pic!");
		    }
		else
			{
			$("#notify").html("no-new");
			}
                error_sleep_time = 500;
                poll();
            },
            error: function() {
                error_sleep_time *= 2;
                setTimeout(poll, error_sleep_time);
            }
        });
    }
    poll();
});

// get latest pic
function getnewpic()
{
  $.get("/getnewpic", function(result){
    $("#new").prepend(result)
  });
};

// load older pic
function loadmorepic()
{
  $.get("/loadmore", function(result){
    $("#more").append(result)
  });
};

//add comments
function addcomment(add_button_id)
{
  var div_id ="#divs" + add_button_id + "c";
  $(div_id).slideToggle("slow");
};

//submit comments
function submitcomment(submit_button_id)
{
function getCookie(name) 
{
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
});


    var main_id = "#m" + submit_button_id;
    var div_id = "#div" + submit_button_id + "c";
    var text_id = "#t" + submit_button_id;
    var word = $(#text_id).val(); //获取文本框的输入
    data={
        comment:word,
        _xsrf:getCookie("_xsrf"),
        id:submit_button_id
        }
    $.post("/addcomment", data, function(result,status){
            if(status == "success")
            {
		$(main_id).append(result)
            }
            else
            {
                alert("提交 失败");
            }
        });
        $(div_id).fadeOut();
};

//cancel comments
function cancelcomment(cancel_button_id)
{
    var div_id = "#divs" + submit_button_id;
    $(div_id).fadeOut();
};

