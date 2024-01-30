$("a.rename").click(function(){
    let id = $(this).attr("id");
    let form_id = $(this).parent().attr("id");
    $("form#"+form_id).children().show();
    $(this).hide();
  });

$("a.rename_close").click(function(){
    let id = $(this).attr("id");
    let form_id = $(this).parent().attr("id");

    $("form#"+form_id).children().hide();
    $(this).hide();
    $(this).siblings("a").show();
  });
  

