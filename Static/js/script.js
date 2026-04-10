function confirmDelete() {
    return confirm("Are you sure you want to delete this product?");
}

function productAdded() {
    alert("Product added successfully!");
}

function validateForm() {
    const name = document.forms["addForm"]["name"].value;
    const quantity = document.forms["addForm"]["quantity"].value;
    const price = document.forms["addForm"]["price"].value;

    if (name == "" || quantity == "" || price == "") {
        alert("Please fill in all fields!");
        return false;
    }

    if (quantity <= 0 || price <= 0) {
        alert("Quantity and Price must be greater than 0");
        return false;
    }

    productAdded();
    return true;
}

function showToast(message, type = "info") {
    let toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add("show");
    }, 100);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 500);
    }, 2500);
}

// Highlight low stock rows on dashboard
window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".low-stock").forEach(el => {
        el.closest("tr").style.backgroundColor = "#fff3cd";
    });

    // Add smooth scroll to top button if not present
    if (!document.getElementById("scrollTopBtn")) {
        let btn = document.createElement("button");
        btn.id = "scrollTopBtn";
        btn.innerText = "↑ Top";
        btn.style.position = "fixed";
        btn.style.bottom = "30px";
        btn.style.right = "30px";
        btn.style.display = "none";
        btn.onclick = () => window.scrollTo({ top: 0, behavior: "smooth" });
        document.body.appendChild(btn);
        window.addEventListener("scroll", () => {
            btn.style.display = window.scrollY > 200 ? "block" : "none";
        });
    }
});