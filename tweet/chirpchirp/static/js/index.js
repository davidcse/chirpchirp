//toggles form to create user
function createUserMode(){
  $(".collapse").show();
  $(".addUser").hide();
  $("#submit-login").text("Create Account");
  $("#main-form").attr("action","/addUser");
}

//toggles form to log in user
function loginUserMode(){
  $(".collapse").hide();
  $(".addUser").show();
  $("#submit-login").text("Log In");
  $("#main-form").attr("action","/login");
}

//clear after submit
function refreshFields(){
  $("#messageDiv").text('');
  $("#usernameField").val('');
  $("#passwordField").val('');
  $("#emailField").val('');
  $("#messageDiv").hide();
}


$( document ).ready(function() {
  // should not display, since no error messages to client upon loading
  $("#messageDiv").hide();

  //should be redirecting to user account creation rest endpoint
  $(".addUser").click(function(){
    createUserMode();
  });


  $("#submit-login").click(function(e){
    e.preventDefault();
    $.ajax({
			type: "post",
			url:$("#main-form").attr("action"),
      data:{
        "username":$("#usernameField").val(),
        "password":$("#passwordField").val(),
        "email":$("#emailField").val()
      },
			timeout: 2000
		}).done(function(data){
      refreshFields();
      //check if redirects to another page
      if(data.redirect && typeof(data.redirect)== "string"){
        window.location.replace(data.redirect);
      }else if(data.message && typeof(data.message) =='string'){
        $("#messageDiv").text(data.message);
        $("#messageDiv").show();
        var mode = $("#main-form").attr("action");
        if(mode =="/addUser" && data.message.includes("Verification")){
          loginUserMode();
        }
      }
		});
  });

});
