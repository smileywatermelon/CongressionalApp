console.log("script ok")

const themeToggle = document.getElementById("theme");
const themeIcon = document.getElementById("themeIcon")

let likesList = document.getElementsByClassName("LIKE");
let commentsList = document.getElementsByClassName("COMMENT");

if (colorMode = "colorMode=dark") {
  document.documentElement.setAttribute('data-bs-theme','dark');
  themeIcon.src = "../../static/sun.svg";
} else {
  document.documentElement.setAttribute('data-bs-theme','light');
  themeIcon.src = "../../static/moon.svg";
}
themeToggle.addEventListener('click',()=>{
    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        document.documentElement.setAttribute('data-bs-theme','light');
        themeIcon.src = "../../static/moon.svg";
        document.cookie = "colorMode=light"
    }
    else {
        document.documentElement.setAttribute('data-bs-theme','dark');
        themeIcon.src = "../../static/sun.svg";
        document.cookie = "colorMode=dark"
    }
})
