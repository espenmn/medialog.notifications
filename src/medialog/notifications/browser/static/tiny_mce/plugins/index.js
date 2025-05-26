tinymce.PluginManager.add('mentions_autocomplete', function(editor) {
  const portalUrl = document.body.getAttribute('data-portal-url') || '';
  const mentionsUrl = portalUrl + '/@mentions_view';

  editor.ui.registry.addAutocompleter('mentions', {
    trigger: '@',
    minChars: 1,
    columns: 1,
    fetch: function (pattern) {
      return fetch(mentionsUrl, {
        headers: {
          'Accept': 'application/json'
        }
      })
        .then(res => res.json())
        .then(users => {
          return users
            .filter(u => u.key.toLowerCase().includes(pattern.toLowerCase()))
            .map(u => ({
              value: '@' + u.value,
              text: u.key
            }));
        });
    },
    onAction: function (autocompleteApi, rng, value) {
      editor.selection.setRng(rng);
      editor.insertContent(value + ' ');
      autocompleteApi.hide();
    }
  });
});
