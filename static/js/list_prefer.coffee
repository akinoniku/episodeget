$(document).ready ->
    $( ".sortable" ).sortable({
      axis: "y"
      placeholder: "ui-state-highlight"
      opacity: 0.6
      scroll: true
      revert: true
    })
    $( ".sortable" ).disableSelection()
    $( ".p-sort" ).sortable({
      axis: "x"
      cursor: 'move'
    })
    $( ".p-sort" ).disableSelection()