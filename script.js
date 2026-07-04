// ======================================
// Resumora AI - Main JavaScript
// ======================================

console.log("Welcome to Resumora AI 🚀");

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function(e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if(target){
            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

// Animate statistics
const statNumbers = document.querySelectorAll(".stat-box h2");

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            const stat = entry.target;

            const finalText = stat.innerText;

            const finalValue = parseInt(finalText.replace(/\D/g,""));

            if(!finalValue) return;

            let count = 0;

            const speed = Math.ceil(finalValue / 100);

            const interval = setInterval(()=>{

                count += speed;

                if(count >= finalValue){

                    stat.innerText = finalText;

                    clearInterval(interval);

                }else{

                    if(finalText.includes("%"))
                        stat.innerText = count + "%";

                    else if(finalText.includes("+"))
                        stat.innerText = count + "+";

                    else
                        stat.innerText = count;

                }

            },20);

            observer.unobserve(stat);

        }

    });

});

statNumbers.forEach(stat=>{
    observer.observe(stat);
});

// Scroll effect for navbar

window.addEventListener("scroll",()=>{

    const navbar = document.querySelector(".navbar");

    if(window.scrollY>50){

        navbar.style.boxShadow="0 10px 25px rgba(0,0,0,.15)";

    }else{

        navbar.style.boxShadow="0 4px 15px rgba(0,0,0,.08)";

    }

});

// Welcome message

window.onload=()=>{

    console.log("Resumora AI Loaded Successfully.");

};
