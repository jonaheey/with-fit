    // More API functions here:
    // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose
let status = 0;
    // the link to your model provided by Teachable Machine export panel
    async function init() {
        
        LoadingWithMask('../static/img/pacman.gif');
        const modelURL = "../static/json/model.json";
        const metadataURL = "../static/json/metadata.json";

        const sign_modelURL = "../static/json/OkModel/model.json";
        const sign_metadataURL = "../static/json/OkModel/metadata.json";

        let error_point = 0
        
        
        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // Note: the pose library adds a tmPose object to your window (window.tmPose)
        model = await tmPose.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();
        maxPredictions2 = model.getTotalClasses();

        sign_model = await tmPose.load(sign_modelURL, sign_metadataURL);
        sign_maxPredictions = sign_model.getTotalClasses();

        // Convenience function to setup a webcam
        const size = 600;
        const flip = true; // whether to flip the webcam
        webcam = new tmPose.Webcam(size, size, flip); // width, height, flip

        try{
            await webcam.setup();
            await webcam.play(); // request access to the webcam
        } catch {
            error_point = 1
        }

        // 웹캠 에러가 발생하지 않은 경우에만 실행
        if (error_point == 0) {
            setTimeout("closeLoadingWithMask()", 3000);
        }
        
        window.requestAnimationFrame(loop);
        
        // append/get elements to the DOM
        const canvas = document.getElementById("canvas");
        canvas.width = size; canvas.height = size;
        ctx = canvas.getContext("2d");
        
        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) { // and class labels
            labelContainer.appendChild(document.createElement("div"));
            }
        
        labelContainer2 = document.getElementById("label-container2");
        for (let i = 0; i < maxPredictions2; i++) { // and class labels
            labelContainer2.appendChild(document.createElement("div"));
            }
        

        // setInterval(함수, 시간) : 주기적인 실행
        const timer = setInterval(function() {
            if(game_switch == 1){
                document.getElementById('timer').style.fontSize = '40px';
                document.getElementById('timer').innerHTML = time;
                
                if (time <= 10) {
                    document.getElementById('timer').style.color = 'red';
                }
                
                time--;

                // 타임아웃 시
                if (time < 0) {
                    clearInterval(timer); // setInterval() 실행을 끝냄
                    document.getElementById('timer').innerHTML = '끝!';
                        }
            }
        
        }, 1000);
    }

    async function loop(timestamp) {
        webcam.update();
        if (game_switch == 0){
            await sign_predict();
        } else if (game_switch == 1) {
            await predict();
        }
        window.requestAnimationFrame(loop);
    }

    async function predict() {
        // Prediction #1: run input through posenet
        // estimatePose can take in an image, video or canvas html element
        webcam_player1 = crop(webcam.canvas, {x: 0, y: 0}, {x: 300, y: 600});
        webcam_player2 = crop(webcam.canvas, {x: 300, y: 0}, {x: 600, y: 600});

        const pose_player1 = await model.estimatePose(webcam_player1);
        const pose_player2 = await model.estimatePose(webcam_player2);
        //console.log(pose_player1.pose.keypoints)

        // Prediction 2: run input through teachable machine classification model
        const prediction = await model.predict(pose_player1.posenetOutput);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction = prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }

        const prediction2 = await model.predict(pose_player2.posenetOutput);
        for (let i = 0; i < maxPredictions2; i++) {
            const classPrediction2 = prediction2[i].className + ": " + prediction2[i].probability.toFixed(2);
            labelContainer2.childNodes[i].innerHTML = classPrediction2;
        }

        pose_detect(prediction);
        pose_detect(prediction2);

        // finally draw the poses
        drawPose(pose_player1.pose, pose_player2.pose);
    }

    async function sign_predict() {
        // Prediction #1: run input through posenet
        // estimatePose can take in an image, video or canvas html element
        webcam_player1 = crop(webcam.canvas, {x: 0, y: 0}, {x: 300, y: 600});
        webcam_player2 = crop(webcam.canvas, {x: 300, y: 0}, {x: 600, y: 600});

        const sign_pose_player1 = await sign_model.estimatePose(webcam_player1);
        const sign_pose_player2 = await sign_model.estimatePose(webcam_player2);

        // Prediction 2: run input through teachable machine classification model
        const sign_prediction1 = await sign_model.predict(sign_pose_player1.posenetOutput);
        const sign_prediction2 = await sign_model.predict(sign_pose_player2.posenetOutput);
        console.log('현재실행')

        if (sign_prediction1[0].probability.toFixed(2) >= 0.99 || sign_prediction2[0].probability.toFixed(2) >= 0.99){
            sign_switch = 0;
            console.log(sign_prediction1[0])
            $(".msg-text").text("서로 준비가 완료되면 화면을 보고 🙆");
        } else if (sign_prediction1[2].probability.toFixed(2) >= 0.60 || sign_prediction1[3].probability.toFixed(2) >= 0.60 && sign_prediction2[2].probability.toFixed(2) >= 0.60 || sign_prediction2[3].probability.toFixed(2) >= 0.60){
            sign_switch = 1;
            $(".msg-text").text("1P & 2P 자리를 잡아주세요.");
        } else if (sign_prediction1[2].probability.toFixed(2) >= 0.60 || sign_prediction1[3].probability.toFixed(2) >= 0.60){
            sign_switch = 1;
            $(".msg-text").text("1P 자리를 잡아주세요.");
        } else if (sign_prediction2[2].probability.toFixed(2) >= 0.60 || sign_prediction2[3].probability.toFixed(2) >= 0.60){
            sign_switch = 1;
            $(".msg-text").text("2P 자리를 잡아주세요.");
        }
        
        if (sign_prediction1[1].probability.toFixed(2) >= 0.99 && sign_prediction2[1].probability.toFixed(2) >= 0.99 && sign_switch == 0)
        {   
            $(".msg-text").text("");
            game_switch = 1;
        }
        
        // finally draw the poses
        drawPose(sign_pose_player1.pose, sign_pose_player2.pose);
    }

    function pose_detect(prediction) {
        const attack = 50;
        let score = 0;
        var audio_pose = new Audio('../static/sound/Kommy_BasicAttack_Hit.wav');
        var audio_set = new Audio('../static/sound/Kommy_BasicAttack.wav');

        if (prediction[0].probability.toFixed(2) >= 0.80 && status == 0) {
                status = 1;
                score = 10 * (prediction[0].probability.toFixed(2) * 100);
        } else if (prediction[1].probability.toFixed(2) >= 0.90 && status == 1) {
                status = 2;
                score = 10 * (prediction[1].probability.toFixed(2) * 100);
                audio_pose.play();
        } else if (prediction[0].probability.toFixed(2) >= 0.80 && status == 2) {
                status = 3;
                score = 10 * (prediction[0].probability.toFixed(2) * 100);
        } else if (prediction[2].probability.toFixed(2) >= 0.90 && status == 3) {
                status = 4;
                score = 10 * (prediction[2].probability.toFixed(2) * 100);
                audio_pose.play();
        } else if (prediction[0].probability.toFixed(2) >= 0.80 && status == 4) {
                status = 0;
                score = 10 * (prediction[0].probability.toFixed(2) * 100);
                damage(attack);
                audio_set.play();
        }
        result_score += score;
        console.log(monster_index)
        if (time <= 0 || monster_index == 4) {
            gameover()
        }
        console.log(status, result_score);
    }

    function gameover(){
        // DB에서 Best_score/Id를 불러와서
        // if (Best_score < result_score){ DB result_score값 저장 }

        window.location.href = '../result';
    }

    function drawPose(pose, pose2) {
     
        if (webcam.canvas) {
            ctx.drawImage(webcam.canvas, 0, 0);
            // draw the keypoints and skeleton
            if (pose && pose2) {
                const minPartConfidence = 0.5;
                for (i=0; i < pose2.keypoints.length; i++){
                    pose2.keypoints[i].position.x = pose2.keypoints[i].position.x + 300;
                }
                tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
                tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
                tmPose.drawKeypoints(pose2.keypoints, minPartConfidence, ctx);
                tmPose.drawSkeleton(pose2.keypoints, minPartConfidence, ctx);
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

    

