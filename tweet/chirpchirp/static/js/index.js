//toggles form to create user
function createUserMode(){
  refreshFields();
  $(".collapse-email").show();
  $(".addUser").hide();
  $("#submit-login").text("Create Account");
  $("#main-form").attr("action","/adduser");
}

//toggles form to log in user
function loginUserMode(){
  refreshFields();
  $(".collapse-email").hide();
  $(".addUser").show();
  $("#submit-login").text("Log In");
  $("#main-form").attr("action","/login");
}


//toggles from verify mode to submission mode
function submissionMode(){
  console.log("setting up submission mode")
  refreshFields();
  $(".submission-container").show();
  $(".verify-account-container").hide();
  loginUserMode();
}


//toggles from submission mode to verify mode
function verifyUserMode(){
  console.log("setting up verification mode")
  refreshFields();
  $(".submission-container").hide();
  $(".verify-account-container").show();
}


//clear after submit
function refreshFields(){
  //clear submission fields
  $("#messageDiv").text('');
  $("#usernameField").val('');
  $("#passwordField").val('');
  $("#emailField").val('');
  $("#messageDiv").hide();
  //clear verification fields
  $("#verifyEmailField").val('');
  $("#verifyKeyField").val('');
}

function submitLoginHandler(){
    $("#submit-login").click(function(e){
      e.preventDefault();
      $.ajax({
  			type: "post",
  			url:$("#main-form").attr("action"),
        data:JSON.stringify({
          "username":$("#usernameField").val(),
          "password":$("#passwordField").val(),
          "email":$("#emailField").val()
        }),
  			timeout: 2000
  		}).done(function(data){
        refreshFields();
        console.log("received from server:"+ JSON.stringify(data));
        //check if redirects to another page
        if(data.redirect && typeof(data.redirect)== "string"){
          window.location.replace(data.redirect);
        }else if(data.error && typeof(data.error) =='string'){
          $("#messageDiv").text(data.error);
          $("#messageDiv").show();
        }else if($("#main-form").attr("action") =="/adduser" && data.status== "OK"){
          loginUserMode();
        }
  		});
    });
}

function verifyAccountHandler(){
  $("#submit-verify").click(function(e){
    e.preventDefault();
    $.ajax({
      type: "post",
      url:$("#verify-form").attr("action"),
      data:JSON.stringify({
        "email":$("#verifyEmailField").val(),
        "key":$("#verifyKeyField").val()
      }),
      timeout: 2000
    }).done(function(data){
      refreshFields();
      console.log("received from server:"+ JSON.stringify(data));
      //check if redirects to another page
      if(data.redirect && typeof(data.redirect)== "string"){
        window.location.replace(data.redirect);
      }else if(data.error && typeof(data.error) =='string'){
        submissionMode();
        $("#messageDiv").text(data.error);
        $("#messageDiv").show();
      }else if(data.status== "OK"){
        submissionMode();
        $("#messageDiv").text("verified successfully, please log in");
        $("#messageDiv").show();
      }
    });
  });
}

$( document ).ready(function() {
  //default is submission mode
  $(".submission-container").show();
  // should not display, since no error messages to client upon loading
  $("#messageDiv").hide();
  //should be redirecting to user account creation rest endpoint
  $(".addUser").click(function(){
    createUserMode();
  });
  // should show forms to input activation key.
  $(".verifyUser").click(function(){
    verifyUserMode();
  });

  //assign login handler
  submitLoginHandler();
  verifyAccountHandler();

});
