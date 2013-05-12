$(document).ready ->
    $( ".sortable" ).sortable({ placeholder: "ui-state-highlight" })
    $( ".sortable" ).disableSelection()
    $( ".p-sort" ).sortable()
    $( ".p-sort" ).disableSelection()
