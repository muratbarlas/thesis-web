
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
        if (data && Object.keys(data).length === 2) {
        // Update the image source
        $('#resizedImage').attr('src', data.image_url);
        $('#string-display').text(data.first_string);}
        else{
            $('#resizedImage_right').attr('src', data.image_url_r);
            $('#string-display_right').text(data.right_string);
            $('#resizedImage').attr('src', data.image_url);
            $('#string-display').text(data.first_string);
        }
    //console.log("heyy")
    }).fail(function() {
        console.log(data.image_url)
        console.error('Failed to load next image.');
    });
}

function loadNext_right() {
    // Make an AJAX request to get the next image URL
     $.get('/next_right', function(data){
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
    console.log("heyy2")
    }).fail(function() {

        console.error('Failed to load next image.');
    });

}

document.addEventListener("keydown", function(event) {
    // Check if the pressed key is the left arrow key
    if (event.key === "ArrowLeft"|| event.key === "a") {
        // Your code to handle left arrow key press goes here
        //console.log("Left arrow key pressed");
        loadNext()
        stopAnimation()
        animate()
    }
});

document.addEventListener("keydown", function(event) {
    // Check if the pressed key is the left arrow key
    if (event.key === "ArrowRight"|| event.key === "b") {
        // Your code to handle left arrow key press goes here
        //console.log("Left arrow key pressed");
        loadNext_right()
        stopAnimation_right()
        animate_right()
    }
});