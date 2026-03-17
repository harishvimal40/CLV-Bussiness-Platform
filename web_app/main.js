/* === DATA STORE === */
const products = [
    # Electronics
    { id: 1, name: "Apple MacBook Air M2", img: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&q=80", price: 99900, disc: 12, rating: 4.8, cat: "Electronics" },
    { id: 2, name: "iPhone 15 Pro Max", img: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80", price: 159900, disc: 5, rating: 4.9, cat: "Electronics" },
    { id: 3, name: "Samsung S24 Ultra", img: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80", price: 129999, disc: 8, rating: 4.8, cat: "Electronics" },
    { id: 4, name: "Sony WH-1000XM5", img: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80", price: 26990, disc: 15, rating: 4.7, cat: "Electronics" },
    { id: 5, name: "Sony Bravia 55' 4K", img: "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=400&q=80", price: 62990, disc: 20, rating: 4.6, cat: "Electronics" },
    { id: 6, name: "Dell XPS 13 Plus", img: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&q=80", price: 145000, disc: 10, rating: 4.5, cat: "Electronics" },
    { id: 7, name: "LG 1.5 Ton AC", img: "https://images.unsplash.com/photo-1621262479599-2780e159079f?w=400&q=80", price: 35990, disc: 25, rating: 4.4, cat: "Electronics" },
    { id: 8, name: "Canon EOS R50", img: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&q=80", price: 75990, disc: 10, rating: 4.7, cat: "Electronics" },

    # Fashion
    { id: 11, name: "Nike Air Jordan 1", img: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", price: 16995, disc: 0, rating: 4.8, cat: "Fashion" },
    { id: 12, name: "Adidas Ultraboost", img: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", price: 12999, disc: 15, rating: 4.6, cat: "Fashion" },
    { id: 13, name: "Ray-Ban Aviator", img: "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&q=80", price: 6590, disc: 10, rating: 4.5, cat: "Fashion" },
    { id: 14, name: "Levi's 511 Jeans", img: "https://images.unsplash.com/photo-1542272617-08f08630329e?w=400&q=80", price: 2899, disc: 30, rating: 4.2, cat: "Fashion" },
    { id: 15, name: "Gucci Leather Bag", img: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&q=80", price: 85000, disc: 5, rating: 4.9, cat: "Fashion" },
    { id: 16, name: "Fossil Gen 6", img: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80", price: 18995, disc: 20, rating: 4.4, cat: "Fashion" },

    # Home
    { id: 19, name: "IKEA Poang Chair", img: "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=400&q=80", price: 8990, disc: 10, rating: 4.6, cat: "Home" },
    { id: 20, name: "Wakefit Ortho Bed", img: "https://images.unsplash.com/photo-1505693416388-b0346efee535?w=400&q=80", price: 12999, disc: 25, rating: 4.7, cat: "Home" },
    { id: 21, name: "Philips Smart LED", img: "https://images.unsplash.com/photo-1507473888900-52e1adad5459?w=400&q=80", price: 1299, disc: 40, rating: 4.4, cat: "Home" },
    { id: 22, name: "Royal Oak Sofa", img: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&q=80", price: 32990, disc: 30, rating: 4.3, cat: "Home" },

    # Beauty & Sports
    { id: 23, name: "Dior Sauvage", img: "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&q=80", price: 14500, disc: 5, rating: 4.9, cat: "Beauty" },
    { id: 24, name: "MAC Ruby Woo", img: "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&q=80", price: 1850, disc: 10, rating: 4.6, cat: "Beauty" },
    { id: 26, name: "MRF Cricket Bat", img: "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400&q=80", price: 8500, disc: 15, rating: 4.7, cat: "Sports" },
    { id: 27, name: "Vector X Football", img: "https://images.unsplash.com/photo-1614632537190-23e4146777db?w=400&q=80", price: 999, disc: 20, rating: 4.2, cat: "Sports" },
    { id: 28, name: "Firefox Bike", img: "https://images.unsplash.com/photo-1532298229144-0ec0c57df56c?w=400&q=80", price: 15990, disc: 10, rating: 4.5, cat: "Sports" }
];

let cart = [];
let currentUser = null; // null or email string

/* === LOGIN LOGIC === */
function sendOtp() {
    const email = document.getElementById('login-email').value;
    if (!email) return alert("Please enter email/mobile");

    document.getElementById('otp-btn').innerText = "Resend OTP";
    document.getElementById('otp-section').classList.remove('hidden');
    alert("OTP sent to " + email + " (Use 1234)");
}

function verifyLogin() {
    const otp = document.getElementById('login-otp').value;
    if (otp === "1234") {
        currentUser = document.getElementById('login-email').value;
        const name = currentUser.split('@')[0];
        document.getElementById('login-overlay').classList.add('hidden');
        document.getElementById('main-app').classList.remove('hidden');

        // Update Navbar
        const btn = document.getElementById('user-display');
        btn.innerText = name;
        btn.style.background = "#2874f0";
        btn.style.color = "white";
        btn.style.border = "none";

        renderProducts(products); // Render All
    } else {
        alert("Invalid OTP");
    }
}

function guestLogin() {
    currentUser = "Guest";
    document.getElementById('login-overlay').classList.add('hidden');
    document.getElementById('main-app').classList.remove('hidden');
    renderProducts(products);
}

function logout() {
    currentUser = null;
    location.reload();
}

/* === RENDERING === */
function renderProducts(list) {
    const grid = document.getElementById('product-grid');
    grid.innerHTML = "";
    document.getElementById('product-count').innerText = list.length;

    list.forEach(p => {
        const afterDis = Math.floor(p.price * (1 - p.disc / 100));
        const card = document.createElement('div');
        card.className = "product-card";
        card.innerHTML = `
            <div class="prod-img-box"><img src="${p.img}" alt="${p.name}"></div>
            <div class="prod-title">${p.name}</div>
            <div class="prod-rating">${p.rating} ★</div>
            <div class="prod-price">₹${afterDis.toLocaleString()} <del>₹${p.price}</del> <span class="prod-discount">${p.disc}% off</span></div>
            <button onclick="addToCart(${p.id})" style="width:100%;margin-top:10px;padding:8px;background:#ff9f00;border:none;color:white;font-weight:600;cursor:pointer;">ADD TO CART</button>
        `;
        grid.appendChild(card);
    });
}

/* === FILTERS === */
function filterCat(cat) {
    let filtered;
    if (cat === 'Mobiles' || cat === 'Electronics') {
        filtered = products.filter(p => p.cat === 'Electronics');
    } else if (cat === 'Appliances') {
        filtered = products.filter(p => p.cat === 'Home' || p.cat === 'Electronics');
    } else {
        filtered = products.filter(p => p.cat === cat);
    }
    renderProducts(filtered);
}

function applyFilters() {
    const max = document.getElementById('price-range').value;
    document.getElementById('max-price-disp').innerText = `₹${parseInt(max).toLocaleString()}`;

    // Simple filter logic
    const filtered = products.filter(p => {
        const price = p.price * (1 - p.disc / 100);
        return price <= max;
    });
    renderProducts(filtered);
}

function handleSearch(txt) {
    txt = txt.toLowerCase();
    const filtered = products.filter(p => p.name.toLowerCase().includes(txt));
    renderProducts(filtered);
}

/* === CART LOGIC === */
function addToCart(id) {
    const p = products.find(i => i.id === id);
    cart.push(p);
    updateCartIcon();
    alert("Added " + p.name);
}

function updateCartIcon() {
    document.getElementById('cart-count').innerText = cart.length;
    document.getElementById('sidebar-count').innerText = cart.length;

    // Render Sidebar
    const body = document.getElementById('cart-body');
    body.innerHTML = "";
    let total = 0;
    cart.forEach((p, idx) => {
        const price = Math.floor(p.price * (1 - p.disc / 100));
        total += price;
        const row = document.createElement('div');
        row.style.cssText = "display:flex;justify-content:space-between;border-bottom:1px solid #eee;padding:10px 0;";
        row.innerHTML = `
            <div style="font-size:14px;width:70%">${p.name}<br><b>₹${price.toLocaleString()}</b></div>
            <button onclick="remCart(${idx})" style="background:none;border:none;color:red;cursor:pointer;">Remove</button>
        `;
        body.appendChild(row);
    });
    document.getElementById('cart-total').innerText = `₹${total.toLocaleString()}`;
}

function remCart(idx) {
    cart.splice(idx, 1);
    updateCartIcon();
}

function toggleCart() {
    document.getElementById('cart-sidebar').classList.toggle('open');
}

/* === CHECKOUT === */
function openCheckout() {
    if (!currentUser) return alert("Please Login First");
    if (cart.length === 0) return alert("Cart Empty");
    toggleCart(); // Close sidebar
    document.getElementById('checkout-modal').style.display = 'flex';
    selectPay('upi'); // Default
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function selectPay(mode) {
    const total = document.getElementById('cart-total').innerText;
    const view = document.getElementById('payment-details-view');
    view.innerHTML = "";

    // Highlight selected
    document.querySelectorAll('.pay-method').forEach(el => el.style.border = '1px solid #eee');
    // (In a real app, we'd add active class here)

    if (mode === 'upi') {
        view.innerHTML = `
            <div style="text-align:center;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=shop@rayan&am=${total.replace(/[^0-9]/g, '')}" alt="QR">
                <p>Scan with GPay / PhonePe / Paytm</p>
                <button onclick="confirmPay()" style="background:#2874f0;color:white;padding:10px;border:none;width:100%;margin-top:10px;">I Have Paid</button>
            </div>
        `;
    } else if (mode === 'card') {
        view.innerHTML = `
            <input type="text" placeholder="Card Number" style="width:100%;padding:10px;margin:5px 0;border:1px solid #ddd;">
            <div style="display:flex;gap:10px;">
                <input type="text" placeholder="MM/YY" style="width:50%;padding:10px;margin:5px 0;border:1px solid #ddd;">
                <input type="password" placeholder="CVV" style="width:50%;padding:10px;margin:5px 0;border:1px solid #ddd;">
            </div>
            <button onclick="confirmPay()" style="background:#fb641b;color:white;border:none;padding:12px;width:100%;font-weight:bold;">PAY ${total}</button>
        `;
    } else if (mode === 'net') {
        view.innerHTML = `
            <select style="width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;">
                <option>HDFC Bank</option><option>SBI</option><option>ICICI Bank</option><option>Axis Bank</option>
            </select>
            <button onclick="confirmPay()" style="background:#2874f0;color:white;border:none;padding:12px;width:100%;">Proceed to Bank</button>
        `;
    } else {
        view.innerHTML = `
            <div style="padding:20px;text-align:center;color:#555;">
                <i class="fa-solid fa-money-bill" style="font-size:30px;color:green;"></i>
                <p>Pay cash at your doorstep.</p>
                <small>+ ₹50 Handling Fee</small>
            </div>
            <button onclick="confirmPay()" style="background:#fb641b;color:white;border:none;padding:15px;width:100%;font-weight:bold;">CONFIRM ORDER</button>
        `;
    }
}

function confirmPay() {
    const total = document.getElementById('cart-total').innerText;
    const id = "OD" + Math.floor(Math.random() * 1000000000);
    alert(`🎉 Order Placed Successfully!\n\nOrder ID: ${id}\nAmount: ${total}`);
    cart = [];
    updateCartIcon();
    closeModal('checkout-modal');
}

/* === AI CHAT === */
function toggleChat() {
    const b = document.getElementById('chat-box');
    b.style.display = b.style.display === 'flex' ? 'none' : 'flex';
    if (b.style.display === 'flex') addAiMsg("Hello! Need help choosing a product?", 'bot');
}

function handleAiEnter(e) { if (e.key === 'Enter') sendAiMsg(); }

function sendAiMsg() {
    const i = document.getElementById('ai-input');
    const txt = i.value.trim();
    if (!txt) return;
    addAiMsg(txt, 'usr');
    i.value = "";

    // Fake logic
    setTimeout(() => {
        let resp = "I can help you compare products!";
        const t = txt.toLowerCase();
        if (t.includes('laptop') || t.includes('macbook')) resp = "The **MacBook Air M2** is our best seller at ₹99,900. Great for work!";
        else if (t.includes('phone') || t.includes('iphone')) resp = "Check out the **iPhone 15 Pro Max** for the best camera experience.";
        else if (t.includes('off') || t.includes('sale')) resp = "We have flat 50-80% Off on Fashion & Electronics!";
        else if (t.includes('track')) resp = "Please go to 'My Orders' to track your shipment.";
        addAiMsg(resp, 'bot');
    }, 600);
}

function addAiMsg(txt, cls) {
    const d = document.createElement('div');
    d.className = "chat-msg " + cls;
    d.innerHTML = txt; // Allow HTML for bolding
    const b = document.getElementById('chat-body');
    b.appendChild(d);
    b.scrollTop = b.scrollHeight;
}

/* === CAROUSEL AUTO === */
let slideIdx = 0;
setInterval(() => {
    moveSlide(1);
}, 5000);

function moveSlide(n) {
    const slides = document.querySelectorAll('.carousel-slide');
    if (slides.length === 0) return;
    slides[slideIdx].classList.remove('active');
    slideIdx = (slideIdx + n + slides.length) % slides.length;
    slides[slideIdx].classList.add('active');
}
