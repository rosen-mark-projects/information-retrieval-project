$(document).ready(function() {
    $('#tweetSubmit').click(searchTweets);

    function searchTweets() {
        var text = $.trim($('#tweetText').val());
        $.ajax({
            url: 'http://localhost:5000/tweets',
            type: 'GET',
            data: {
                text: text
            },
            success: function(data){
                console.log(data)
            },
            error: function(data){

            }
        });
    }
});