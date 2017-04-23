/*
 *NOTE: WARNING THAT THIS FILE IS HIGHLY DEPENDENT AND COUPLED WITH :
 * UPLOADFORM.JS
 * THIS AND UPLOADFORM.JS CAN BE MERGED INTO ONE FILE, BUT FOR READABILITY
 * IS SPLIT UP. MAKE SURE BOTH ARE INCLUDED INTO THE HTML AS SCRIPTS.
 * THE TWO ARE DEPENDENT ON THE SHARED GLOBAL VARIABLE mediaArray
 */



//check if the global mediaArray is defined, if not define it.
if(typeof(mediaArray)=="undefined"){
  window.mediaArray = [];
}



//get contents of global array of media that has been uploaded.
// after posting the media with this tweet, clear that array
function getMediaArrayIds(){
  var mediaIds = [];
  for(var i=0; i<mediaArray.length; i++){
    mediaIds.push(mediaArray.pop());
  }
  console.log("attaching media ids to tweet:" + JSON.stringify(mediaArray));
  return mediaIds;
}


//send tweet to the server, on response update the tweet feed view.
function tweetAjaxPost(tweet){
  console.log("posting tweet: " + tweet + " by :" + username);
  var postdata = JSON.stringify({
    'content': tweet,
    'media' : getMediaArrayIds()
  });
  console.log("sending this in posted body :"+JSON.stringify(postdata));
  $.ajax({
    type: "post",
    url: "/additem",
    data: postdata,
    timeout: 2000
  }).done(function(response){
    console.log("received from server:" +JSON.stringify(response));
    clearPreviewDiv("#preview-image"); //clear <img>. method defined in uploadForm.js
    //request tweet data that we just posted
    if(response.id){
      ajaxRetrieveTweet(response.id);
    }
  });
}

function ajaxRetrieveTweet(id){
  console.log("GET retrieving tweet: " + id);
  $.ajax({
    type: "get",
    url: "/item/"+id , //get the specific tweet
    timeout: 2000
  }).done(function(response){
    console.log("received from server:" +JSON.stringify(response));
    // renderTweetFeedList(response.username,tweet);
  });
}

//creates a tweet post in the tweet feed section.
function createTweetDomContainer(user,tweet,wellOption){
  var well = "";
  if(wellOption){
    well="well";
  }
  return '\
  <div class="row">\
    <div class="col-sm-3">\
      <div class="'+well+'">\
       <p><strong>@'+username+'<strong></p>\
      </div>\
    </div>\
    <div class="col-sm-9">\
      <div class="'+well+'">\
        <p>'+ tweet + '</p>\
      </div>\
    </div>\
  </div>';
}


//render the view of tweets in tweet feed list
function renderTweetFeedList(username, tweet){
  var listElement = createTweetDomContainer(username,tweet,true);
  $("#tweetFeedList").append(listElement);
}

// get a single tweet by id and render it to itemResult div.
function renderTweetItem(username,tweet){
  $("#itemResult").html(''); // clear previous list elements
  var listElement = createTweetDomContainer(username,tweet,false);
  $("#itemResult").append(listElement);
}

//Handler to post a tweet
function postTweetHandler(){
	$('#postTweetButton').on('click', function(e){
		e.preventDefault();
		var tweetContent = $('#tweetText').val();
    tweetAjaxPost(tweetContent)
    $('#tweetText').val(""); //clear
	});
}

function searchFieldHandler(){
	$("#searchFieldSubmit").click(function(e){
		e.preventDefault();
		var search = $("#searchField").val();
		console.log("searching: "+ search);
		$.ajax({
			type: "post",
			url: "/search",
			data: JSON.stringify({
				"timestamp": search,
				"limit":25
			}),
			timeout: 2000
		}).done(function(data){
			console.log("received from server:"+JSON.stringify(data));
      if(data.status !="OK"){
        console.log("encountered server error");
        return
      }

      for(var i=0;i<data.items.length;i++){
        renderTweetFeedList(data.items[i].username, data.items[i].content);
      }
		});
	});
}


$(document).ready(function(){
  // bind handlers
  postTweetHandler();
});
