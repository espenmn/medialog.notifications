$(document).on('DOMNodeInserted', function(e) {
    var usersFilterCheckbox = $("#form-widgets-user_filter-0");
    var timeFilterCheckbox = $("#form-widgets-time_filter-0");

    var fields = {
        users: [
            $("#formfield-form-widgets-message_users"),
            $("#formfield-form-widgets-message_groups"),
            $("#formfield-form-widgets-additional_users")
        ],
        time: [
            $("#formfield-form-widgets-relative_time"),
            $("#formfield-form-widgets-effective_date")
        ]
    };


    function toggleFields(checkbox, fieldsGroup) {
        fieldsGroup.forEach(field => field.toggle(!checkbox.is(":checked")));        
    }

    // Initialize visibility on page load
    toggleFields(usersFilterCheckbox, fields.users);
    toggleFields(timeFilterCheckbox, fields.time);

    // Add event listeners to the checkboxes
    usersFilterCheckbox.on("change", () => toggleFields(usersFilterCheckbox, fields.users));
    timeFilterCheckbox.on("change", () => toggleFields(timeFilterCheckbox, fields.time));

    
});

