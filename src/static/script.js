let button = document.querySelector('button');
let fileInput = document.querySelector('#test_img');
let upload_img = document.querySelector('#upload_img');
let upload_img_text = document.querySelector('#upload_img_text');
let predict = document.querySelector('#predict')
let animal_info = document.querySelector("#animal_info");
let example_container = document.getElementById('example_container');
let animal_heading = document.querySelector('#animal_heading')
let animal_image = document.querySelector("#animal_images")
let speak_btn = document.querySelector("#speak_btn");

speak_btn.style.display="None";
animal_heading.style.display = "None"
animal_image.style.display = "None"
upload_img.style.display='None'
upload_img_text.style.display='None'
let file = null


fileInput.onchange  = function(){
    file = fileInput.files[0];

    console.log(file);
    if(file){
        let imageURL = URL.createObjectURL(file);
        console.log('asdf', imageURL)
        upload_img.src = imageURL;
        upload_img_text.style.display='block';
        upload_img.style.display = 'block'; 
        upload_img.style.height= '400px';
        upload_img.style.width = '500px';

    }
}

button.onclick = function(){
    let formData = new FormData();
    formData.append('image',file)

    fetch('/predict',{
        method: 'POST',
        body: formData
    })
    .then(response=>response.json())
    .then(data=>{
        let prediction = data.prediction
        predict.textContent = prediction
        fetchAnimalDetails(prediction)
    })

}
async function fetchAnimalDetails(animal_name) {
    console.log("Animal name:", animal_name);
    try {
        const response = await fetch(`/fetch_animal_details/${animal_name}`);
        const data = await response.json();
        console.log(data);
        console.log('test', data.extract);
        console.log('titl',data.images);

        animal_heading.style.display = 'block';
        animal_heading.innerText = `${animal_name} Information`
        animal_info.innerText = data.extract;
        example_container.innerHTML = "";
        animal_image.innerText = "";
        speak_btn.style.display='block';
        if(data.extract == "Sorry No infromation available") return ;
        

        animal_image.style.display = 'block';
        animal_image.innerText = `${animal_name} Images`
        
        data.images.forEach(title=>{
            let imgElement = document.createElement('img');
            imgElement.src = `https://en.wikipedia.org/wiki/Special:FilePath/${title.replace('File:', '')}`;
            imgElement.alt=title;
            imgElement.width=200;
            example_container.appendChild(imgElement);
        })
    } catch (error) {
        console.error("Error:", error);
    }
}


//speak 
let pause = false;
speak_btn.onclick = function(){
    pause = !pause;
    if(pause){
        speak_btn.innerText = "Stop";
        speak_btn.classList.add('blow-up');
        let msg = new SpeechSynthesisUtterance(animal_info.innerText)
        msg.lang = 'en-US';
        msg.rate=0.9;
        msg.pitch=0.4;
        window.speechSynthesis.speak(msg);
        msg.onend = function(){
            speak_btn.innerText = "Play";
            speak_btn.classList.remove('blow-up');    
            pause=false;
        }
    }else{
        window.speechSynthesis.cancel();
        speak_btn.innerText = "Play";
        speak_btn.classList.remove('blow-up');
    }
    

}


window.onload = function () {
    window.speechSynthesis.cancel(); // Stop any ongoing speech when the page loads
};
