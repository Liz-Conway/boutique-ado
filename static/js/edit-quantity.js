// Update quantity on click
$(".updateLink").onclick(updateQuantity);

function updateQuantity(event) {
    /* Use the prev() method to find the most recently seen ".updateForm" in the Dom*/
    let form = this.prev(".updateForm");
    /*Call the forms submit method*/
    form.submit();
}

// Remove item & reload on click
$(".removeLink").onclick(removeQuantity);

/*Post some data to a URL
Once the response comes back from the server,
 reload the page to reflect the updated bag*/
function removeQuantity(event) {
    /*CSRF token which we can store as a string by just rendering it here.
    NB this uses the actual template variable with the double curly brackets.
    As opposed to the template tag which uses the inner percent signs.
    This is because the former renders the actual token.
    While the latter renders a hidden input field in a form.*/
    // let csrfToken = "{{ csrf_token }}";
    let csrfToken = getCSRF();
    /*prodId can be obtained by splitting the ID of the update link being clicked on
    and taking the second half of it.*/
    let prodId = $(this).attr("id").split("remove")[1];
    /*Use the data() method to pull the size from the data-size attribute*/
    let size = $(this).data("size");
    let url = `/bag/remove/${prodId}`;
    /*data = the object we'll use to send this data to the server.
    The data variable will contain a special key called "csrfmiddlewaretoken",
    which will have our csrfToken variable as its value;
    and the data variable will contain the size.
    The "csrfmiddlewaretoken" key will match the field Django is expecting
    to see in request.POST when we post it to the server.*/
    let data = {"csrfmiddlewaretoken": csrfToken, "size": size};

    /*Use the post method from jQuery.
    Giving it both the URL and the data.*/
    $.post(url, data)
        /*When done -> execute a function to reload the page.*/
        .done(function() {
            location.reload();
        });
}

/*https://www.hacksoft.io/blog/quick-and-dirty-django-passing-data-to-javascript-without-ajax*/
function getCSRF() {
    let selector = "input[name='csrfmiddlewaretoken']";
    return JSON.parse(document.querySelector(selector).getAttribute('value'));
}
