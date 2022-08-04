

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelectorAll('.btn_like').forEach(element => {
        element.addEventListener('click', (evt) => {
            
            post_id = evt.target.dataset.postid
            fetch('/post/' + post_id,{
                method: 'PUT',
                body: JSON.stringify({
                  'post_id': post_id,
                  'liked': "False"
                })
            })
            .then(response => ()=>{
                console.log("Inside the js response")
                console.log(response)
                response.json()
            })
            .then(result => {
                evt.target.src = result.liked ?  "/static/network/img/red.png" : "/static/network/img/translike.png" 
                likes_span = evt.target.nextElementSibling
                likes_span.innerHTML = result.count_likes == "None" ? likes_span.innerHTML : result.count_likes
            })
        });
    })
    

});
