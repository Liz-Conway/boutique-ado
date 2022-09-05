    // Capture the change event from the sort selector
    $("#sortSelector").change(function() {
        var selector = $(this);
        //     Current url which is equal to a new URL object
        // that takes in the current Windows location.
        // Using the URL object will give us some nice functionality in particular
        // the ability to replace the current get parameters which is required in order to
        // update the sorting methodology
        var currentUrl = new URL(window.location);

        var selectedVal = selector.val();

        if(selectedVal != "reset") {
            // The first item from splitting the selected value will be the item we're sorting on.
            var sort = selectedVal.split("_")[0];
            // The second item from splitting the selected value will be the direction either ascending or descending.
            var direction = selectedVal.split("_")[1];

            //  Replace the get parameters in the URL.
            // Using the searchParams.set() method from the URL object.
            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);

            /* Replacing the location will also cause the page to reload which will resort the
            products accordingly */
            window.location.replace(currentUrl);
        } else {
            // If the user has selected the reset option
            // Simply delete the sort and direction get parameters and then replace the location.
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");

            window.location.replace(currentUrl);
        }
    });
