
function startTimer () {
    for (let i = 0; i <= 60; i++) {
        for (let j = 0; j <= 60; j++) {
            setTimeout(() => {
                if (j === 60){
                    document.getElementById("seconds").value = 0;
                    document.getElementById("minutes").value = parseInt(document.getElementById("minutes").value) + 1;
                }
                document.getElementById("seconds").value = parseInt(document.getElementById("seconds").value) + 1;
            }, (i * 60 + j) * 1000); // total elapsed seconds
           
        }
       
    }
}
function stopTimer () {
    location.reload();
}

