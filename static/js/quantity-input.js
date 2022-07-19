$(".incrementQty").click(addQuantity);
$(".decrementQty").click(subtractQuantity);

/*Increment Quantity*/
function addQuantity(event) {
    /*prevent the default button action.*/
    event.preventDefault();
    // closest() method searches up to the parent. And the find() method searches down.
    // So what we're saying here is from the button element go up the tree to the
    // closest inputGroup class.
    // And then drill down to find the first element with the class quantityInput.
    // var closestInput = $(this).closest(".inputGroup").find(".quantityInput")[0];

     /*Find the closest sibling input box to this button*/
    let closestInput = $(this).siblings(".quantityBox");
    /*Cache the value that's currently in the input box in a variable called currentValue*/
    let currentValue = parseInt(closestInput.val());
    /*Use that variable to set the input boxes new value to the current value plus one.*/
    closestInput.val(currentValue + 1);
    /* For some reason Javascript converts the "data" identifier to lower case??????????*/
    let productId = $(this).data("productid");
    handleEnableDisable(productId);
}

/*Decrement Quantity*/
function subtractQuantity(event) {
    event.preventDefault();
    // var closestInput = $(this).closest(".quantityBox");
    let closestInput = $(this).siblings(".quantityBox");
    let currentValue = parseInt(closestInput.val());
    closestInput.val(currentValue - 1);
    let productId = $(this).data("productid");
    handleEnableDisable(productId);
}

/*Each input will be associated with a specific product id.
We can pass that product id into the handleEnableDisable() function.*/
/*Disable +/- buttons outside 1 - 99 range*/
function handleEnableDisable(productId) {
    /*Use the productId to get the current value of the input based on its id attribute.*/
    let currentValue = parseInt($(`#idQty${productId}`).val());
    let minusDisabled = currentValue < 2;
    let plusDisabled = currentValue > 98;
    /*Disable the minus button if the current value is less than two*/
    $(`#decrementQty${productId}`).prop('disabled', minusDisabled);
    /*Disable the plus button if the current value is more than 98*/
    $(`#incrementQty${productId}`).prop('disabled', plusDisabled);
}

/*Since the default of the input box is 1
It allows us to click the minus button and potentially add a quantity of 0 to the bag.
The input elements min and Max will prevent this via form validation.
But let's add a couple more pieces of functionality just to solidify this*/

/*First we can disable the minus button by default.
By getting all the quantity inputs on the page & Iterating through them.
For each one calling the enable/disable function as soon as the page loads.*/
let allQtyInputs = $("[class$='crementQty']");
/*Ensure proper enabling/disabling of all inputs on page load*/
for(let i =0; i < allQtyInputs.length; i++) {
    let productId = $(allQtyInputs[i]).data("productid");
    handleEnableDisable(productId);
}

/*Call the handle enable/disable function
if the user uses the built-in up and down arrows in the number box to change the quantity.
by listening to the change event on the quantity input*/
/*Check enable/disable every time the input is changed*/
$("[class$='crementQty']").change(function() {
    let productId = $(this).data("productid");
    handleEnableDisable(productId);
});
