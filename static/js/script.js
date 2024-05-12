
//////////////////left anim
const box = document.getElementById('resizedImage') // Get the element we want to animate.
const coords = {x: 0, y: 400}
let animationID;
const tween = new TWEEN.Tween(coords, false) // Create a new tween that modifies 'coords'.
	.to({x: 0, y: 0}, 2000) // Move to (300, 200) in 1 second.
	.easing(TWEEN.Easing.Quadratic.InOut) // Use an easing function to make the animation smooth.
	.onUpdate(() => {
			// Called after tween.js updates 'coords'.
			// Move 'box' to the position described by 'coords' with a CSS translation.
		box.style.setProperty('transform', 'translate(' + coords.x + 'px, ' + coords.y + 'px)')
		//console.log(coords)

	})
	.onComplete(function() {
      // Stop the tween when it completes
     // console.log("complete")
      coords.x = 0
      coords.y = 0
      //tween.stop();

    })
	.start() // Start the tween immediately.

// Setup the animation loop.
function animate(time) {
    //console.log("animating")
	tween.update(time)
	animationID = requestAnimationFrame(animate)
}

// Call this function to start the animation loop
function startAnimation() {
    if (!animationID) {
        animate();
    }
}
// Call this function to stop the animation loop
function stopAnimation() {
    cancelAnimationFrame(animationID);
    animationID = null;
    tween.stop()
    //console.log("stopped")
    //console.log(coords_right)
    tween.to({x: 0, y: 0}, 1)
    tween.stop()
    tween.to({x: 0, y: 0}, 800)
    tween.start()
}
/////////////////////////////////////right anim
const box_right = document.getElementById('resizedImage_right') // Get the element we want to animate.
const coords_right  = {x: 0, y: 400}
let animationID_right;
const tween_right = new TWEEN.Tween(coords_right, false) // Create a new tween that modifies 'coords'.
	.to({x: 0, y: 0}, 2000) // Move to (300, 200) in 1 second.
	.easing(TWEEN.Easing.Quadratic.InOut) // Use an easing function to make the animation smooth.
	.onUpdate(() => {
			// Called after tween.js updates 'coords'.
			// Move 'box' to the position described by 'coords' with a CSS translation.
		box_right.style.setProperty('transform', 'translate(' + coords_right.x + 'px, ' + coords_right.y + 'px)')
		//console.log(coords_right)

	})
	.onComplete(function() {
      // Stop the tween when it completes
     // console.log("complete")
      coords_right.x = 0
      coords_right.y = 0
      //tween.stop();
    })
	.start() // Start the tween immediately.

function animate_right(time) {
    //console.log("animating_r")
	tween_right.update(time)
	animationID_right = requestAnimationFrame(animate_right)
}


function startAnimation_right() {
    if (!animationID_right) {
        animate_right();
    }
}

// Call this function to stop the animation loop
function stopAnimation_right() {
    cancelAnimationFrame(animationID_right);
    animationID_right = null;
    tween_right.stop()
    //console.log("stoppedr")
    //console.log(coords_right)
    tween_right.to({x: 0, y: 0}, 1)
    tween_right.stop()
    tween_right.to({x: 0, y: 0}, 800)
    tween_right.start()
}
////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function() {
    var nextButton = document.getElementById('nextButton');
    var imageElement = document.getElementById('resizedImage');
    nextButton.addEventListener('click', function() {
        stopAnimation()
        animate()
    });
});

function loadNext() {
    // Make an AJAX request to get the next image URL
    $.get('/next', function(data) {
        // Check if the server response contains a redirect URL
        if (data.redirect) {
            // Redirect the browser to the specified URL
            window.location.href = data.redirect;
        } else {
            // Handle the normal response with image and text updates
            if (data && Object.keys(data).length === 2) {
                // If response has 2 keys, assume it's the first set of images/text
                $('#resizedImage').attr('src', data.image_url);
                $('#string-display').text(data.first_string);
            } else {
                // Otherwise handle the second set of images/text
                $('#resizedImage_right').attr('src', data.image_url_r);
                $('#string-display_right').text(data.right_string);
                $('#resizedImage').attr('src', data.image_url);
                $('#string-display').text(data.first_string);
            }
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        // Log the error to the console
        console.error('Failed to load next image: ' + textStatus + ', ' + errorThrown);
    });
}

function loadNext_right() {
    // Make an AJAX request to get the next image URL
     $.get('/next_right', function(data){
         if (data.redirect) {
            // Redirect the browser to the specified URL
            window.location.href = data.redirect;
         } else {
            // Update the image source
             if (data && Object.keys(data).length === 2) {
                $('#resizedImage_right').attr('src', data.image_url_r);
                $('#string-display_right').text(data.right_string);
            } else {
                console.log("got it ")
                console.log(data.first_string)
                $('#resizedImage_right').attr('src', data.image_url_r);
                $('#string-display_right').text(data.right_string);
                $('#resizedImage').attr('src', data.image_url);
                $('#string-display').text(data.first_string);
            }
         }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        // Log the error to the console
        console.error('Failed to load next image: ' + textStatus + ', ' + errorThrown);
    });

}




document.addEventListener("keydown", function(event) {
    // Check if the pressed key is the left arrow key
    if (event.key === "ArrowLeft"|| event.key === "a") {
        $.get('/get_counter', function(data) {
            if (data.counter === 2) {
                // Perform actions if the counter variable is equal to 0
                loadNext_right();
                stopAnimation_right();
                animate_right();
                loadNext()
                stopAnimation()
                animate()


            } else  {
                console.log(data.counter)
                loadNext()
                stopAnimation()
                animate()
            }


         }).fail(function() {
            console.error('Failed to get counter value.');
        });

    }
});



document.addEventListener("keydown", function(event) {
    // Check if the pressed key is the right arrow key or the 'b' key
    if (event.key === "ArrowRight" || event.key === "b") {
        // Make an AJAX request to get the value of the counter variable from the Flask server
        $.get('/get_counter', function(data) {
            // Check if the counter variable is equal to 0
            if (data.counter === 2) {
                // Perform actions if the counter variable is equal to 0
                loadNext_right();
                stopAnimation_right();
                animate_right();
                loadNext()
                stopAnimation()
                animate()

            } else  {
                console.log(data.counter)
                loadNext_right()
                stopAnimation_right()
                animate_right()
            }
        }).fail(function() {
            console.error('Failed to get counter value.');
        });
    }
});