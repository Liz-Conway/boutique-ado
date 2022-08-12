/**
	Core logic for this comes from:
	https://stripe.com/docs/payments/accept-a-payment

	CSS from :
	https://stripe.com/docs/stripe-js
 */

/*Stripe works with what are called payment intents.
The process will be that when a user hits the checkout page
1) the checkout view will call out to stripe and create a payment intent
for the current amount of the shopping bag.
When stripe creates it, the payment intent will also have a secret that identifies it.
2) This secret will be returned to us and we'll send it to the template as the client_secret variable.
3)Then in the JavaScript on the client side.
We'll call the confirmCardPayment() method from stripe js,
using the client_secret which will verify the card number.
*/

/*Those little script elements contain the values we need as their text.
So we can get them just by getting their ids and using the .text function.
I'll also slice off the first and last character on each
since they'll have quotation marks which we don't want.*/
let stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
let clientSecret = $("#id_client_secret").text().slice(1, -1);

console.log('Stripe Public Key', stripePublicKey);
console.log('Initial Client Secret', clientSecret);

/*Style taken from
https://stripe.com/docs/js/appendix/style*/
let style = {
	base: {
		iconColor: '#c4f0ff',
		color: '#000',
		fontWeight: '500',
		fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
		fontSize: '16px',
		fontSmoothing: 'antialiased',
		':-webkit-autofill': {
			color: '#fce883',
		},
		'::placeholder': {
			color: '#87BBFD',
		},
	},
	invalid: {
		iconColor: '#E84610',
		color: '#E84610',
	},
}

/*Made possible by the stripe js included in the base template.
All we need to do to set up stripe is create a variable using our stripe public key*/
let stripe = Stripe(stripePublicKey);
// console.log('stripe variable :  ', stripe);
/*Create an instance of stripe elements.*/
let elements = stripe.elements();
console.log('elements variable :  ', elements);
/*Use "elements" to create a card element.*/
/*The card element can also accept a style argument.*/
let card = elements.create('card', {"style": style});
console.log('card variable :  ', card);

/*Mount the card element to the div we created in checkout.html*/
card.mount("#stripeCard");


// Handle realtime validation errors on the card element
card.addEventListener('change', handleCardChange);

function handleCardChange(event) {
	let errorDiv = $("#stripeError");

	if(event.error) {
		let html = `
			<span class="icon" role="alert">
				<i class="fas fa-times"></i>
			</span>
			<span>${event.error.message}</span>
		`;
		$(errorDiv).html(html);
	} else {
		errorDiv.textContext = "";
	}
}

// Handle form submit
let form = document.getElementById('paymentForm');

form.addEventListener('submit', formSubmit);

function formSubmit(event) {
	console.log("Submitting the form");
	console.log('Client Secret', clientSecret);
	/* STEP 1
	 * When the user clicks the submit button
	  * the event listener prevents the form from submitting
	 * and instead disables the card element and triggers the loading overlay.*/
	event.preventDefault();
	/*Disable both the card element and the submit button
	 to prevent multiple submissions.*/
    card.update({ 'disabled': true});
    $('#submitButton').attr('disabled', true);
	/*Trigger the overlay and fade out the form when the user clicks the submit*/
    $('#paymentForm').fadeToggle(100);
    $('#loadingOverlay').fadeToggle(100);

	/* STEP 2
	 * Create a few variables to capture the form data
	 * we can't put in the payment intent here,
	 * and instead post it to the cacheCheckoutData view*/
	/*Get the boolean value of the "saveInfo" box by looking at its "checked" attribute*/
	let saveInfo = Boolean($('#saveInfo').attr('checked'));
    // From using {% csrf_token %} in the form
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
	/*Create a small object to pass this information to the new view.
	Also pass the client secret for the payment intent.*/
	let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
	/*Create a variable for the new URL*/
    // let url = '/checkout/cache-checkout-data/';
	let url = '/checkout/cacheCheckoutData/';

	/*Post this data to the view.
	Use our trusty post() method built into jQuery
	Telling it we're posting to the URL and that we want to post the "postData" above.*/
	/*Wait for a response that the PaymentIntent was updated before calling the confirmCardPayment() method
	Just tack on the .done() method and	execute the callback function*/
    $.post(url, postData).done(function () {
	console.log('Before confirmCardPayment()', clientSecret);
	/* STEP 3
	 * The view updates the payment intent and returns a 200 response,
	 * at which point we call the confirmCardPayment() method from stripe
	 * and if everything is ok submit the form.*/
		/*Will be executed if our view returns a 200 response*/
		stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
					/*only added postcode to the shipping information
					since the billing postal code will come from the card element and
					stripe will override it if we try to add it anyway*/
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
			/* STEP 3a
			 * If there's an error in the form
			 * then the loading overlay will be hidden,
			 * the card element re-enabled and the error displayed for the user.*/
			if (result.error) {
				console.log("Error calling confirmCardPayment()")
                let errorDiv = document.getElementById('stripeError');
                let html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
				/*Show the form and fade out the overlay when there is an error*/
                $('#paymentForm').fadeToggle(100);
                $('#loadingOverlay').fadeToggle(100);
				/*If there's an error.
				Re-enable the card element and the submit button
				 to allow the user to fix it*/
                card.update({ 'disabled': false});
                $('#submitButton').attr('disabled', false);
            } else {
				console.log("Successfully called confirmCardPayment()");
				console.log("Status :  ", result.paymentIntent.status)
				console.log("Result : \n", result);
                if (result.paymentIntent.status === 'succeeded') {
					console.log("Payment intent succeeded");
					form.submit();
                }
            }
        });
		/* STEP 3b
		If anything goes wrong posting the data to our view
		Reload the page and display the error without ever charging the user*/
    }).fail(function () {
		/*Failure function, which will be triggered
		if our view sends a 400 bad request response*/
        // just reload the page, the error will be in django messages
        location.reload();
    })
}
