tinymce.PluginManager.add('mentions_autocomplete', function(editor) {
  editor.ui.registry.addAutocompleter('mentions', {
    trigger: '@', 
    ch: '@',
    minChars: 1,
    columns: 1,
    fetch: function (pattern) {
      return fetch('/@@mentions_view')
        .then(res => res.json())
        .then(users => {
          return users
            .filter(u => u.key.includes(pattern))
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
