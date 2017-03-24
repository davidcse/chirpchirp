//send tweet to the server
function tweetAjaxPost(tweet){
  console.log("posting tweet: " + tweet + " by :" + username);
  $.ajax({
    type: "post",
    url: "/additem",
    data: JSON.stringify({'content': tweet}),
    timeout: 2000
  }).done(function(response){
    console.log("received from server:" +JSON.stringify(response))
    renderTweetFeedList(username,tweet)
  });
}

//show the tweet in list
function renderTweetFeedList(username, tweet){
  var listElement = '<li> <strong>' + username + ': </strong>' + tweet + '</li><br>';
  $("#tweetFeedList").append(listElement);
}

// get a single tweet by id and render it to itemResult div.
function renderTweetItem(username,tweet){
  $("#itemResult").html(''); // clear previous list element
  $("#itemResult").append(listElement);
  var listElement = '<li> <strong>' + username + ': </strong>' + tweet + '</li><br>';
  $("#itemResult").append(listElement);
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


function searchItemHandler(){
  $("#searchItem").click(function(e){
    e.preventDefault();
    var tweetId = $("#searchItemField").val();
    console.log("getting /item: "+ tweetId);
    $.ajax({
      type: "get",
      url: "/item/"+tweetId,
      timeout: 2000
    }).done(function(data){
      console.log("received from server:"+JSON.stringify(data));
      if(data.status !="OK"){
        console.log("encountered server error");
        return
      }
      renderTweetItem(data.item.username, data.item.content);
    });
  });
}

$(document).ready(function(){
  postTweetHandler();
  searchFieldHandler();
  searchItemHandler();
});
