// Update quantity on click
$(".updateLink").click(updateQuantity);

function updateQuantity(event) {
    /*Use the closest() method to find the parent of the updateLink button (it is a "div")*/
    /* Use the prev() method to find the previous sibling element of the div
     *  IF it has a class of ".updateForm"*/
    let form = $(this).closest("div").prev(".updateForm");
    /*Call the form's submit method*/
    form.submit();
}

// Remove item & reload on click
$(".removeLink").click(removeQuantity);

/*Post some data to a URL
Once the response comes back from the server,
 reload the page to reflect the updated bag*/
function removeQuantity(event) {
    /* NB this uses the actual template variable with the double curly brackets.
    As opposed to the template tag which uses the inner percent signs.
    This is because the former renders the actual token.
    While the latter renders a hidden input field in a form.*/
    // let csrfToken = "{{ csrf_token }}";

    /*CSRF token which we can store as a string by just rendering it here. */
    let csrfToken = getCSRF();
    /*prodId can be obtained by splitting the ID of the update link being clicked on
    and taking the second half of it.*/
    let prodId = $(this).attr("id").split("remove")[1];
    /*Use the data() method to pull the size from the data-productSize attribute*/
    /*For some reason JS converts the data attribute to lowercase*/
    let size = $(this).data("productSize".toLowerCase());
    let url = `/bag/remove/${prodId}`;
    /*data = the object we'll use to send this data to the server.
    The data variable will contain a special key called "csrfmiddlewaretoken",
    which will have our csrfToken variable as its value;
    and the data variable will contain the size.
    The "csrfmiddlewaretoken" key will match the field Django is expecting
    to see in request.POST when we post it to the server.*/
    let data = {"csrfmiddlewaretoken": csrfToken, "productSize": size, "whatever": 'dude'};

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
    let element = document.querySelector(selector);
    let value = element.getAttribute('value');
    //return JSON.parse(value);
    return value;
}
