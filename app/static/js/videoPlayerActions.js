function likeVideo(button, videoId) {
    $.post("/likeVideo", {videoId: videoId})
    .done(function(data) {
        
        var likeButton = $(button);
        var dislikeButton = $(button).siblings(".dislikeButton");

        likeButton.addClass("active");
        dislikeButton.removeClass("active");

        var result = data;
        updateLikesValue(likeButton.find(".text"), result.likes);
        updateLikesValue(dislikeButton.find(".text"), result.dislikes);

        if(result.likes < 0) {
            likeButton.removeClass("active");
            likeButton.find("img:first").attr("src", "/static/images/icons/thumb-up.png");
        }
        else {
            likeButton.find("img:first").attr("src", "/static/images/icons/thumb-up-active.png")
        }

        dislikeButton.find("img:first").attr("src", "/static/images/icons/thumb-down.png");
    });
}

function dislikeVideo(button, videoId) {
    $.post("/dislikeVideo", {videoId: videoId})
    .done(function(data) {
        
        var dislikeButton = $(button);
        var likeButton = $(button).siblings(".likeButton");

        dislikeButton.addClass("active");
        likeButton.removeClass("active");

        var result = data;
        updateLikesValue(likeButton.find(".text"), result.likes);
        updateLikesValue(dislikeButton.find(".text"), result.dislikes);

        if(result.dislikes < 0) {
            dislikeButton.removeClass("active");
            dislikeButton.find("img:first").attr("src", "/static/images/icons/thumb-down.png");
        }
        else {
            dislikeButton.find("img:first").attr("src", "/static/images/icons/thumb-down-active.png")
        }

        likeButton.find("img:first").attr("src", "/static/images/icons/thumb-up.png");
    });
}

function updateLikesValue(element, num) {
    var likesCountVal = element.text() || 0;
    element.text(parseInt(likesCountVal) + parseInt(num));
}