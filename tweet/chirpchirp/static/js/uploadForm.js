//check if the global mediaArray is defined, if not define it.
if(typeof(mediaArray)=="undefined"){
  window.mediaArray = [];
}

//give the image div a src to display and render, unhide image divs.
function bindPreview(imagePreviewDiv, localUrl){
  $(imagePreviewDiv).attr('src', localUrl);
  $("#preview-image-container").show();
}

//give the image div a src to display and render, unhide image divs.
function clearPreviewDiv(imagePreviewDiv){
  $(imagePreviewDiv).attr('src', "#");
  $(imagePreviewDiv).attr('target', "");
  $("#preview-image-container").hide();
}

function sendPhoto(formdata){
  $.ajax({
      url: '/addmedia',
      data: formdata,
      cache: false,
      contentType: false,
      processData: false,
      type: 'POST',
      success: function(data){
          if(data.id){
            //store the media id as part of the global mediaArray, for tweet posts attachments.
            mediaArray.push(data.id);
            //store the media id as part of the image preview, for dynamic delete.
            $("#preview-image").attr("target",data.id);
            console.log("updated global mediaArray:" + JSON.stringify(mediaArray));
          }
          alert(JSON.stringify(data));
      }
  });
}

function readLocalFile(input) {
    if (input.files && input.files[0]) {
        console.log("preview of image");
        var reader = new FileReader();
        reader.onload = function (e) {
          bindPreview("#preview-image",e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function uploadInputHandler(){
  $("#upload-photo").change(function(){
      readLocalFile(this);
      //post the input data to the server
      var formData = new FormData();
      formData.append("content",this.files[0]);
      console.log("posting image");
      console.log(formData);
      console.log(this.files[0]);
      sendPhoto(formData);
  });
}

function removeFromMediaArray(id){
  for(var i=0;i<mediaArray.length;i++){
    if(id==mediaArray[i]){
      mediaArray.splice(i,1); //removes one element at position,i.e. target media ID
      break;
    }
  }
}

function deleteUploadHandler(deleteButtonDiv, imageDiv){
  $(deleteButtonDiv).on('click',function(){
    var mediaId = $(imageDiv).attr('target');
    removeFromMediaArray(mediaId);
    clearPreviewDiv(imageDiv);
  });
}

$(document).ready(function(){
  uploadInputHandler();
  $("#preview-image-container").hide();
  deleteUploadHandler("#delete-preview-image","#preview-image");
});
