//send tweet to the server
function tweetAjaxPost(tweet){
  console.log("posting tweet: " + tweet);
  $.ajax({
    type: "post",
    url: "/additem",
    data: JSON.stringify({'content': tweet}),
    timeout: 2000
  }).done(function(response){
    console.log("received from server:" +JSON.stringify(response))
    renderTweetFeedList(tweet)
  });
}

//show the tweet in list
function renderTweetFeedList(tweet){
  var listElement = '<li>'+ tweet +'</li><br>'
  $("#tweetFeedList").append(listElement);
}

//Handler to post a tweet
function postTweetHandler(){
	$('#postTweetButton').on('click', function(e){
		e.preventDefault();
		var tweetContent = $('#tweetText').val();
    tweetAjaxPost(tweetContent)
	});
  console.log("tweethandler ready");
}

$(document).ready(function(){
  postTweetHandler();
});
