document.getElementById("fileInput").addEventListener("change", uploadFile);

function uploadFile(event) {
    let file = event.target.files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerHTML = `
            <p>Material: ${data.material}</p>
            <p>Confidence: ${data.confidence}</p>
            <p>Price: ${data.price}</p>
        `;
        });
}
