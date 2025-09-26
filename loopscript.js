 for (let x = 0; x < 10; x++) {
    if (x==5){
    console.log("We're halfway there!");
  } else{
    console.log(x);
  }
  }


  function calculate(num1, num2, operation) {
    let value;
    if (operation === "plus") { 
    value = parseInt(num1) + parseInt(num2);
    } else if (operation === "minus") {
      value = parseInt(num1) - parseInt(num2);
    } else if (operation === "multiply") {
      value = parseInt(num1) * parseInt(num2);
    } else if (operation === "divide") {
      value = parseInt(num1) / parseInt(num2);
    } else {
      value = "Invalid operation";
    }
document.getElementById("result").innerText = value;
  }

function loopFunction() {
  for (let i = 0; i < 1000; i++) {
    setTimeout(() => {
      document.getElementById("loop-result").innerText = i;
    }, i * 100); 
  }
}
