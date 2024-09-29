/* Тястично взял код с stack overflow */
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("modal");
    const closeBtn = document.getElementById("closeBtn");
    const tryNowBtn = document.getElementById("tryNow");

    setTimeout(function() {
        modal.style.display = "flex";
    }, 3000);

    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    tryNowBtn.onclick = function() {
        alert("Перенаправляем на страницу загрузки лаунчера!");
        window.location.href = "/launcher";
        modal.style.display = "none";
    }
});
/* Тястично взял код с stack overflow */
