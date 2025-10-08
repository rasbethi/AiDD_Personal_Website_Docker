// dynamic year
const y = document.getElementById("year");
if (y) y.textContent = new Date().getFullYear();

// hamburger menu
const burger = document.querySelector(".hamburger");
const nav = document.querySelector(".nav");
if (burger && nav) {
    burger.addEventListener("click", () => {
        const open = nav.classList.toggle("open");
        burger.setAttribute("aria-expanded", String(open));
    });
}

// reveal on scroll
const revealables = document.querySelectorAll("[data-reveal]");
const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add("revealed"); io.unobserve(e.target); }
    });
}, { threshold: .12 });
revealables.forEach(el => io.observe(el));

// sliders (simple)
function wireSlider(id) {
    const root = document.getElementById(id);
    if (!root) return;
    const track = root.querySelector(".slides");
    const prev = root.querySelector(".prev");
    const next = root.querySelector(".next");
    const step = () => track.clientWidth * 0.9;
    prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
}
wireSlider("homeSlider");
wireSlider("projSlider");

// contact form validation
const form = document.getElementById("contactForm");
if (form) {
    const first = document.getElementById("firstName");
    const last = document.getElementById("lastName");
    const email = document.getElementById("email");
    const pass = document.getElementById("password");
    const conf = document.getElementById("confirmPassword");

    const setErr = (input, msg) => {
        const row = input.closest(".form-row");
        const area = row && row.querySelector(".error");
        if (area) area.textContent = msg || "";
    };

    form.addEventListener("submit", (e) => {
        let ok = true;
        setErr(first, ""); setErr(last, ""); setErr(email, ""); setErr(pass, ""); setErr(conf, "");

        if (!first.value.trim()) { setErr(first, "first name is required"); ok = false; }
        if (!last.value.trim()) { setErr(last, "last name is required"); ok = false; }

        const epat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value.trim()) { setErr(email, "email is required"); ok = false; }
        else if (!epat.test(email.value)) { setErr(email, "enter a valid email"); ok = false; }

        if (pass.value.length < 8) { setErr(pass, "at least 8 characters"); ok = false; }
        if (conf.value !== pass.value) { setErr(conf, "passwords must match"); ok = false; }

        if (!ok) { e.preventDefault(); }
    });
}

document.getElementById('contactForm').addEventListener('submit', function (e) {
    const pw = document.getElementById('password');
    const cpw = document.getElementById('confirmPassword');
    const errorSpan = cpw.nextElementSibling;

    if (pw.value !== cpw.value) {
        e.preventDefault(); // stop submission
        errorSpan.textContent = "Passwords must match";
        cpw.focus();
    } else {
        errorSpan.textContent = "";
    }
});
