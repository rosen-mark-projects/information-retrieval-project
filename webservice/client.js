$(document).ready(function() {
    $('#tweetSubmit').click(searchTweets);

    function searchTweets() {
        var keyword = $.trim($('#tweetText').val());
        $.ajax({
            url: 'http://localhost:5000/tweets',
            type: 'GET',
            data: {
                text: keyword
            },
            success: function(data){
                console.log(data)
                $('#tweetsContainer').empty()
                var htmlRender = `  <div class="row">
                                        <div class="col-sm-12 text-center">
                                            <br>
                                            <p>You searched tweets, related to <b><i>${keyword}</i></b></p>
                                        </div>
                                    </div>`;
                data.forEach(element => {
                    htmlRender += `<div class="row">
                                        <div class="col"></div>
                                        <div class="col-12">
                                            <hr>
                                            <p>${element.text}</p>
                                            <a href="${element.url}">${element.url}</a>
                                            <p>Truth: ${element.target === 1 ? 'Yes' : 'No'}</p>
                                        </div>
                                        <div class="col"></div>
                                    </div>`
                });
                $('#tweetsContainer').append(htmlRender);
            },
            error: function(data){
                console.log(data)
            }
        });
    }
});
