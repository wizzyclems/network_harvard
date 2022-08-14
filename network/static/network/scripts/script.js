

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelectorAll('.btn_like').forEach(element => {
        element.addEventListener('click', (evt) => {
            console.log("the like button was clicked.")
            post_id = evt.target.dataset.postid
            

                fetch('/post/' + post_id,{
                    method: 'PUT',
                    body: JSON.stringify({
                      'post_id': post_id,
                      'liked': "False"
                    })
                })
                .then( (response) =>{
                    json_response = response.json()
                    // console.log(json_response)
                    return json_response
                })
                .then(result => {
                
                    if(result.status == 403 ){
                        console.log("Trigger login for the user")
                        login_modal = $('#loginModal')
                        console.log(login_modal)
                        $('#loginModal').modal()
                        return
                    }

                    if( result.liked ){
                        evt.target.src =  "/static/network/img/red.png" 
                        evt.target.setAttribute("class","mylikes_like btn_like post_meta_items_like")
                    }else{
                        evt.target.src = "/static/network/img/translike.png" 
                        evt.target.setAttribute("class","mylikes_unlike btn_like post_meta_items_unlike")
                    }
                    
                    likes_span = evt.target.nextElementSibling
                    likes_span.innerHTML = result.count_likes == "None" ? likes_span.innerHTML : result.count_likes
                    
                })
                .catch( err => {
                    console.log(`The exception is ${err}`)
                    console.log(`The exception is ${err.message}`)
                })
            
        })
    })


    // if( document.querySelector(".edit_toggle") != null ){
    // This is the click event for the edit button
    document.querySelectorAll('.edit_button').forEach(element => {
        element.addEventListener('click', (evt) => {
            console.log("An edit button was clicked.")
            target_edit_btn = evt.target
            target_post_div = target_edit_btn.parentElement.parentElement.previousElementSibling

            post_id = target_edit_btn.dataset.postid
            console.log(`The post id is ${post_id}`)
            post_content = target_post_div.innerText

            //Extract items from the browsers session storage for re-use.
            cache_data = `{"post_id": "${post_id}", "post_content": "${post_content}"}`
            // cache_data = "{" + post_id + ": " + post_id + ", post_content: " + post_content + "}"
            console.log(cache_data)
            sessionStorage.setItem("post_edit_info", cache_data)

            post_edit_div = document.createElement("div")
            post_edit_div.setAttribute("class", "col-12 post_content")

            textarea_div = document.createElement("div")
            textarea_div.setAttribute("class", "row")
            textarea_div.setAttribute("style", "width:95%")

            textarea = document.createElement("textarea")
            textarea.setAttribute("id", "txtarea_post_edit")
            textarea.setAttribute("class", "form-control")
            textarea.innerHTML = post_content
            textarea.dataset.postid = post_id

            textarea_div.append(textarea)

            buttons_div = document.createElement("div")
            buttons_div.setAttribute("class", "row justify-content-end")
            buttons_div.setAttribute("style", "width:95%")

            cancel_btn = document.createElement("button")
            cancel_btn.innerHTML = "Cancel"
            cancel_btn.setAttribute("class", "btn btn-outline-secondary btn-sm cancel_post_edit")
            cancel_btn.setAttribute("type", "button")
            cancel_btn.setAttribute("style", "margin:5px;")
            cancel_btn.onclick = (evt) => {

                //Retrieve edit info from the browser's session storage
                post_edit_info = JSON.parse(sessionStorage.getItem("post_edit_info"))
                console.log("cancel button clicked")
                console.log(post_edit_info)
                post_id = post_edit_info.post_id
                post_content = post_edit_info.post_content
    
                post_content_div = document.createElement("div")
                post_content_div.setAttribute("class", "post_content")
                post_content_div.innerHTML = post_content
    
                
                target_post_div.replaceChildren()
                target_post_div.append(post_content_div)

                enable_edit_buttons(true)

                sessionStorage.removeItem("post_edit_info")
                
            }

            save_btn = document.createElement("button")
            save_btn.innerHTML = "Save"
            save_btn.setAttribute("type", "button")
            save_btn.setAttribute("class", "btn btn-outline-secondary btn-sm save_post_edit")
            save_btn.setAttribute("style", "margin:5px")
            save_btn.onclick = (evt) => {
                //Get the post content from the browser's session storage and display
                post_edit_info = JSON.parse(sessionStorage.getItem("post_edit_info"))
                console.log("save button clicked")
                console.log(post_edit_info)
                post_id = post_edit_info.post_id
                post_content = document.querySelector("#txtarea_post_edit").value
    
                fetch('/post/edit/' + post_id,{
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: post_id,
                        post_content: post_content
                    })
                })
                .then(response => response.json())
                .then(result => {

                    console.log(`The edit result from the server is : ${result}`)
                    let post_id = result.post_id
                    let message = result.message
                    let status = result.status
                    console.log(`The backend message is ${message}`)

                    post_content_div = document.createElement("div")
                    post_content_div.setAttribute("class", "post_content")
                    post_content_div.innerHTML = post_content

                    target_post_div.replaceChildren()
                    target_post_div.append(post_content_div)

                    enable_edit_buttons(true)

                    sessionStorage.removeItem("post_edit_info")

                })
                
            }

            buttons_div.append(cancel_btn)
            buttons_div.append(save_btn)

            post_edit_div.append(textarea_div)
            post_edit_div.append(buttons_div)

            target_post_div.replaceChildren()
            target_post_div.append(post_edit_div)

            enable_edit_buttons(false)

        })

    })
  
    

})


function enable_edit_buttons(status){
    document.querySelectorAll('.edit_button').forEach(element => {
        if( status ){
            element.style.display = "block"
            // element .removeAttribute("disabled")
            // element.removeAttribute("class")
            // element.setAttribute("class","edit_button mylikes_unlike")
        }else{
            // document.querySelectorAll('.edit_button').forEach(element => {
                // element.setAttribute("disabled","disabled")
                // element.removeAttribute("class")
                // element.setAttribute("class","edit_button disable_edit")
                element.style.display = "none"
            // })
        }
    })
}
