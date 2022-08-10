

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
            
        })
    })


    if( document.querySelector(".edit_toggle") != null ){
            document.querySelector(".edit_toggle").onclick = (evt) => {
            
            target_edit_btn = evt.target
            target_post_div = target_edit_btn.parentElement.nextElementSibling

            post_id = target_edit_btn.dataset.postid
            post_content = target_post_div.innerText

            console.log(`The post id to edit is ${post_id}`)
            console.log(`The post content to edit is ${post_content}`)

            sessionStorage.setItem("post_id", post_id)
            sessionStorage.setItem("post_content", post_content)

            post_edit_div = document.createElement("div")

            textarea_div = document.createElement("div")
            textarea = document.createElement("textarea")
            textarea.setAttribute("id", "txtarea_post_edit")
            textarea.innerHTML = post_content
            textarea.dataset.postid = post_id

            console.log(textarea)

            textarea_div.append(textarea)

            buttons_div = document.createElement("div")

            cancel_btn = document.createElement("button")
            cancel_btn.innerHTML = "Cancel"
            cancel_btn.setAttribute("id", "cancel_post_edit")
            cancel_btn.onclick = (evt) => {

                post_id = sessionStorage.getItem("post_id")
                post_content = sessionStorage.getItem("post_content")
    
                console.log(`The post id to edit is ${post_id}`)
                console.log(`The post content to edit is ${post_content}`)
    
                post_content_div = document.createElement("div")
                post_content_div.setAttribute("id", "post_content")
                post_content_div.innerHTML = post_content
    
                
                target_post_div.replaceChildren()
                target_post_div.append(post_content_div)
                
            }

            save_btn = document.createElement("button")
            save_btn.innerHTML = "Save"
            save_btn.setAttribute("id", "save_post_edit")
            save_btn.onclick = (evt) => {
                //Get the post content from the browser's session storage and display
    
                console.log("The save button was clicked.")
                post_content_edit = document.querySelector("#post_content_edit")
    
                fetch('/post/edit/' + post_id,{
                    method: 'PUT',
                    body: JSON.stringify({
                    'post_id': post_id
                    })
                })
                .then( response.json() )
                .then(result => {
                    
                })
                
            }

            buttons_div.append(cancel_btn)
            buttons_div.append(save_btn)

            post_edit_div.append(textarea_div)
            post_edit_div.append(buttons_div)

            target_post_div.replaceChildren()
            target_post_div.append(post_edit_div)
            console.log("edit text area shoould show now")
            console.log(target_post_div)

        }

    }
  
    

})
