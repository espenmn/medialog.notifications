
$(document).ready(function () {
    var usersFilterCheckbox = $("#form-widgets-user_filter-0");
    var usersField = $("#formfield-form-widgets-message_users");
    var additionalUsers = $("#formfield-form-widgets-additional_users");

    function toggleUsers() {
        if (usersFilterCheckbox.is(":checked")) {
            usersField.hide();
            additionalUsers.hide();
        } else {
            usersField.show();
            additionalUsers.show();
        }
    }

    var timeFilterCheckbox = $("#form-widgets-time_filter-0");
    var relativeTimeField = $("#formfield-form-widgets-relative_time");
    var effectiveTimeField = $("#formfield-form-widgets-effective_date");

    function toggleRelativeTime() {
        if (timeFilterCheckbox.is(":checked")) {
            relativeTimeField.hide();
            effectiveTimeField.hide();
        } else {
            relativeTimeField.show();
            effectiveTimeField.show();
        }
    }

    // Initialize visibility on page load
    toggleRelativeTime();
    toggleUsers();

    // Add event listener to the checkbox to toggle visibility on change
    timeFilterCheckbox.on("change", toggleRelativeTime);
    usersFilterCheckbox.on("change", toggleUsers);
});