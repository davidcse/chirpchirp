var searchedUser = "";


// handler to logout client from session.
function logoutHandler(){
	$("#logoutButton").click(function(){
		console.log("logging out");
		$.ajax({
			type: "post",
			url: "/logout",
			timeout: 2000
		}).done(function(data){
			console.log("received from server:"+JSON.stringify(data))
			window.location.replace(data.redirect);
		});
	});
}


// create dom element to wrap around search results.
function createDomUserProfile(email,following,followers){
  var currSearchUser = $("#profilesearchbar").val()
  var followingUrl="/user/"+currSearchUser+"/following";
  var followersUrl="/user/"+currSearchUser+"/followers";
  return '\
  <br>\
  <div class="well">\
    <button class="btn btn-lg"><span class="glyphicon glyphicon-user"></span></button>\
        <button id="followButton"><span class="glyphicon glyphicon-plus"></span></button>\
        <div>\
            <p class="text-center">\
              Email:<strong>'+email+'<strong>\
            </p>\
            <table class="table">\
              <tr>\
                <td>Followers</td>\
                <td>Following</td>\
              </tr>\
              <tr class = "followTableRowContainer">\
                <td id= "followerCount">\
                  <button class="btn btn-info">\
                  <a href="'+ followingUrl +'">'
                      +following+
                  '</a></button>\
                </td>\
                <td id= "followingCount">\
                  <button class="btn btn-info">\
                  <a href="'+ followersUrl +'">'
                      +followers+
                  '</a></button>\
                </td>\
              </tr>\
            </table>\
        </div>\
  </div>\
  ';
}



//creates dom element and append to user profile list in page.
function renderUserProfileList(data){
  //clear previous user search
  $("#userProfileList").html('');
  if(data.user){
    var followers_count = data.user.followers;
    var following_count = data.user.following;
    var email = data.user.email;
    var userProfileCard = createDomUserProfile(email,following_count,followers_count);
    $("#userProfileList").append(userProfileCard);
  }
}


//print the response object.
function handleServerMessages(data){
  if(data.redirect){
    window.location.replace(data.redirect);
  }else if(data.message){
    console.log("displaying server message");
    $("#serverMessage").html(data.message);
  }else if (data.error){
    console.log("displaying server error");
    $("#serverMessage").html(data.error);
  }
}



//NOTE: div with id followButton is only available when a user profile search returns the DOM element
function followButtonHandler(){
  $("#followButton").click(function(e){
    e.preventDefault();
    console.log("Following user:"+searchedUser);
    $.ajax({
      type: "post",
      url: "/follow",
      data: JSON.stringify({'follow':true,"username":searchedUser}),
      timeout: 2000
    }).done(function(data){
      console.log("received from server:"+JSON.stringify(data));
      handleServerMessages(data);
    });
  });
}

// handler to search bar button.
function userProfileSearchHandler(){
	$("#profilesearchbutton").click(function(e){
    e.preventDefault();
		console.log("trigger search user");
		$.ajax({
			type: "get",
			url: '/user/'+ $("#profilesearchbar").val(),
			timeout: 2000
		}).done(function(data){
			console.log("received from server:"+JSON.stringify(data))
      //render dom with user profile elements
      renderUserProfileList(data);
      handleServerMessages(data);
      //store the currently searched user
      searchedUser = $("#profilesearchbar").val();
      //bind follow button in newly rendered dom.
      followButtonHandler();
		});
	});
}


$(document).ready(function(){
	logoutHandler();
  userProfileSearchHandler();
});
