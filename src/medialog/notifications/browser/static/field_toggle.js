$(document).on('DOMNodeInserted', function (e) {
    var usersFilterCheckbox = $("#form-widgets-user_filter-0");
    var timeFilterCheckbox = $("#form-widgets-time_filter-0");

    var fields = {
        users: [
            $("#formfield-form-widgets-notify_users"),
            $("#formfield-form-widgets-notify_groups"),
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



// //For use with 'mention', if user types @username in TinyMCE or other field

// function fetchMentions(pattern) {
//     const portalUrl = document.body.getAttribute('data-portal-url') || '';
//     const mentionsUrl = portalUrl + '/@mentions_view';
//     return fetch(mentionsUrl, {
//         headers: { 'Accept': 'application/json' }
//     })
//         .then(res => res.json())
//         .then(users => users
//             .filter(u => u.key.toLowerCase().includes(pattern.toLowerCase()))
//             .map(u => ({
//                 value: '@' + u.value,
//                 text: u.key
//             }))
//         );
// }


