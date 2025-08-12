function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please select a file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.detail) {
                alert(data.detail);
            } else {
                document.getElementById("result").innerHTML = `
                <h2>${data.material}</h2>
                <p>Confidence: ${data.confidence}%</p>
                <p>Price: ₹${data.price_per_kg} / kg</p>
            `;
                initMap(data.nearest_shops[0].location);
            }
        })
        .catch(err => console.error(err));
}

function initMap(locationUrl) {
    const latLng = { lat: 28.6139, lng: 77.2090 }; // Example Delhi coords
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: latLng
    });
    new google.maps.Marker({
        position: latLng,
        map: map
    });
}
