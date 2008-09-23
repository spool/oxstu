function edit(name) {

    // change the page layout
    $("#" + name + "-edit-link").addClass('hidden');
    $("#" + name + "-cancel-link").removeClass('hidden');
    $("#" + name + "-label").addClass('hidden');
    $("#" + name + "-edit").removeClass('hidden');

    // set the default value to the current text
    var newval = $("#" + name + "-label").text();
    $("#" + name + "-edit").attr('value', newval);
    $("#" + name + "-edit").focus();

}

function cancel(name) {

    // change the page layout
    $("#" + name + "-edit-link").removeClass('hidden');
    $("#" + name + "-cancel-link").addClass('hidden');
    $("#" + name + "-label").removeClass('hidden');
    $("#" + name + "-edit").addClass('hidden');

}

function save(name) {

    // change the page layout
    $("#" + name + "-edit-link").removeClass('hidden');
    $("#" + name + "-cancel-link").addClass('hidden');
    $("#" + name + "-label").removeClass('hidden');
    $("#" + name + "-edit").addClass('hidden');

    // get the value the user typed in
    var newval = $("#" + name  + "-edit").attr('value');

    // function to be executed if the post succeeds
    onSuccess = function(data) {
        
        // check if we had a validation error
        if ( $("value", xml) ) {

            // set the value on the page
            var resultval = $("value", xml).text();
            $("#" + name + "-label").text(resultval);

        } else {

            // pop-up the error message
            if ( $("error", xml) ) {
                alert( $("error", xml).text() );
            } else {
                alert("Unkown error occured saving data!");
            }

            // put the form back into edit mode
            edit("name");

        }

    };

    // function to be executed if the post fails
    onFailure = function() {

        // pop-up an error
        alert("Could not submit metadata update!");

    };

    // actually do the post (asynchronous - will update controls when complete)
    $.ajax({
        url: "/admin/ajax/story_metadata/",
        data: {name: name, value: newval},
        dataType: "xml",
        error: onFailure,
        success: onSuccess,
        type: "POST"
    });

}

function post_comment(storyid) {

    // get the value the user typed in
    var newval = $("#comment_field").attr('value');

    // check for zero-length
    if ( newval == '' ) return;

    // function to be executed if the post succeeds
    onSuccess = function(data) {
    
        // Yay!
        $("#comment_field").attr('value', '');
        $("#story_comments").load("/admin/frag/story_comments/" + storyid + "/"); 

    };

    // function to be executed if the post fails
    onFailure = function() {

        // pop-up an error
        alert("Could not post comment! (bad)");

    };

    // actually do the post (asynchronous - will update controls when complete)
    $.ajax({
        url: "/admin/frag/story_comments/" + storyid + "/",
        data: {comment: newval},
        dataType: "text",
        error: onFailure,
        success: onSuccess,
        type: "POST"
    });

}

