tinymce.PluginManager.add('mentions_autocomplete', function(editor) {
  editor.ui.registry.addAutocompleter('mentions', {
    trigger: '@',
    minChars: 1,
    columns: 1,
    fetch: fetchMentions,
    onAction: function (autocompleteApi, rng, value) {
      editor.selection.setRng(rng);
      editor.insertContent(value + ' ');
      autocompleteApi.hide();
    }
  });
});
