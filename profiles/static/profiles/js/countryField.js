let defaultCountry = $("id_default_country");
let countrySelected = defaultCountry.val();
/* The value will be an empty string if the first option is selected.
So to determine if that's selected we can use this as a boolean.
So if country selected is false */
if(!countrySelected) {
	/* Set the colour of this element to be that grey placeholder colour */
	defaultCountry.css("color", "#aab7c4")
}
/* Capture the change event. */
defaultCountry.change(function (){
	/* Every time the box changes we'll get the value of it, */
	countrySelected = $(this).val();
	/* And then determine the proper colour */
	if(!countrySelected) {
		defaultCountry.css("color", "#aab7c4")
	} else {
		defaultCountry.css("color", "#000")
	}
});
