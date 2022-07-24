// Call the toast method from bootstrap. With an option of show.
// $(".toast").toast("show");

$(".close").click(closeToast);

function closeToast(event) {
    let toast = $(this).closest("div.toast");
    toast.hide();
}
