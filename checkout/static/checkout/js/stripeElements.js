/**
	Core logic for this comes from:
	https://stripe.com/docs/payments/accept-a-payment

	CSS from :
	https://stripe.com/docs/stripe-js
 */

/*Those little script elements contain the values we need as their text.
So we can get them just by getting their ids and using the .text function.
I'll also slice off the first and last character on each
since they'll have quotation marks which we don't want.*/
let stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
let client_secret = $("#id_client_secret").text().slice(1, -1);

/*Made possible by the stripe js included in the base template.
All we need to do to set up stripe is create a variable using our stripe public key*/
let stripe = Stripe(stripe_public_key);
/*Create an instance of stripe elements.*/
let elements = stripe.elements();
/*Use "elements" to create a card element.*/
let card = elements.create('card');

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

/*The card element can also accept a style argument.*/

/*Mount the card element to the div we created in checkout.html*/
card.mount("#stripeCard", {"style": style});
