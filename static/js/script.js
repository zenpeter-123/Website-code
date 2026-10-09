let lightBox = document.querySelector(".lightbox")
let photos = document.querySelectorAll(".gallery-item")
let lightboxImage = document.querySelector("#lightbox-image")
let closeBtn = document.querySelector("#close-btn")

photos.forEach((pic) => {
  pic.addEventListener("click", () => {
    let endIndex = pic.src.indexOf("-thumbnail")
    if(endIndex != -1){
    lightboxImage.src = pic.src.slice(0, endIndex) + ".jpg"}
    else{lightboxImage.src = pic.src}
    lightBox.style.display = "flex"
  }) 
})

closeBtn.addEventListener("click", () => {
  lightBox.style.display = "none"
})

lightBox.addEventListener("click", () => {
  if(lightBox.style.display != "none"){lightBox.style.display = "none"}
})

const colors = ['rgb(64,224,208)', 'white', 'rgb(80,200,120)'];
const element = document.getElementById('logo');
const sentence = element.textContent.split(' ');

element.innerHTML = sentence
  .map((word, i) => `<span style="color:${colors[i]}">${word}</span>`)
  .join('');



const modals = document.querySelectorAll(".modal-background");
const openModalBtns = document.querySelectorAll(".open-modal");
const closeModalBtns = document.querySelectorAll(".close-modal");

openModalBtns.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    modals[index].classList.add("aktiv")
  })
})

closeModalBtns.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    modals[index].classList.remove("aktiv")
  })
})

modals.forEach((modal) => {
  modal.addEventListener("click", (event) => {
  if (event.target == modal) {
    modal.classList.remove("aktiv")
  }
})

modal.addEventListener("click", (event) => {
  if (event.key == "Escape"){
    modal.classList.remove("aktiv")
  }
})
})
