    // More API functions here:
    // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose

    // the link to your model provided by Teachable Machine export panel

    async function init() {
        const modelURL = "../static/json/model.json";
        const metadataURL = "../static/json/metadata.json";
        
        
        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // Note: the pose library adds a tmPose object to your window (window.tmPose)
        model = await tmPose.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();
        let status = 0

        // Convenience function to setup a webcam
        const size = 600;
        const flip = false; // whether to flip the webcam
        webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
        await webcam.setup(); // request access to the webcam
        await webcam.play();
        window.requestAnimationFrame(loop);
        
        // append/get elements to the DOM
        const canvas = document.getElementById("canvas");
        canvas.width = size; canvas.height = size;
        ctx = canvas.getContext("2d");
        
        // 데미지 관련 변수

        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) { // and class labels
            labelContainer.appendChild(document.createElement("div"));
        }
    }

    async function loop(timestamp) {
        webcam.update();
        await predict();
        window.requestAnimationFrame(loop);
    }

    async function predict() {
        // Prediction #1: run input through posenet
        // estimatePose can take in an image, video or canvas html element
        
        const pose_player1 = await model.estimatePose(webcam.canvas);
        //console.log(pose_player1.pose.keypoints)

        // Prediction 2: run input through teachable machine classification model
        const prediction = await model.predict(pose_player1.posenetOutput);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction = prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }
        pose_detect(prediction)
        // finally draw the poses
        drawPose(pose_player1.pose);
    }

    function pose_detect(prediction) {
        const attack = 10
        var audio_pose = new Audio('../static/sound/Kommy_BasicAttack_Hit.wav');
        var audio_set = new Audio('../static/sound/Kommy_BasicAttack.wav');

        if (prediction[0].probability.toFixed(2) >= 0.90) {
                status = 1
        } else if (prediction[1].probability.toFixed(2) >= 0.90 && status == 1) {
                status = 2
                audio_pose.play();
        } else if (prediction[1].probability.toFixed(2) >= 0.90 && status == 2) {
                status = 3
                audio_pose.play();
        } else if (prediction[2].probability.toFixed(2) >= 0.90 && status == 3) {
                status = 0
                damage(attack);
                audio_set.play();
        }
        console.log(status);
    }

    function drawPose(pose) {
     
        if (webcam.canvas) {
            ctx.drawImage(webcam.canvas, 0, 0);
            // draw the keypoints and skeleton
            if (pose) {
                const minPartConfidence = 0.5;
                tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
                tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
            }
        }
    }

    function crop(can, a, b) {
        // get your canvas and a context for it
        var ctx = can.getContext('2d');
        
        // get the image data you want to keep.
        var imageData = ctx.getImageData(a.x, a.y, b.x, b.y);
      
        // create a new cavnas same as clipped size and a context
        var newCan = document.createElement('canvas');
        newCan.width = b.x - a.x;
        newCan.height = b.y - a.y;
        var newCtx = newCan.getContext('2d');
      
        // put the clipped image on the new canvas.
        newCtx.putImageData(imageData, 0, 0);
      
        return newCan;    
     }