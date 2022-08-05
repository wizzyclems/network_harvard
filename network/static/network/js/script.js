

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
                .then( (response) =>{
                    console.log("Inside the js response")
                    console.log(response)
                    console.log(`Response status : ${response.status}`)
                    console.log(`Response status text : ${response.statusText}`)

                    json_response = response.json()
                    // console.log(json_response)
                    return json_response
                })
                .then(result => {
                    console.log(result.status)
                    console.log(result)
                    if(result.status == 403 ){
                        console.log("Trigger login for the user")
                        login_modal = $('#loginModal')
                        console.log(login_modal)
                        $('#loginModal').modal()
                        return
                    }
                    evt.target.src = result.liked ?  "/static/network/img/red.png" : "/static/network/img/translike.png" 
                    likes_span = evt.target.nextElementSibling
                    likes_span.innerHTML = result.count_likes == "None" ? likes_span.innerHTML : result.count_likes
                    
                })
                .catch( err => {
                    console.log(`The exception is ${err}`)
                    console.log(`The exception is ${err.message}`)
                })
            
        });
    })
    

});
