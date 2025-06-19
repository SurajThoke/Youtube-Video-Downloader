document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const input = document.querySelector("input");
    const resultBox = document.getElementById("result");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const url = input.value;

        resultBox.innerHTML = "<p>Loading...</p>";

        fetch("http://localhost:5000/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: url }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.error) {
                    resultBox.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
                } else {
                    const formats = data.formats
                        .map(
                            (f) =>
                                `<li><a href="${f.url}" target="_blank">${f.ext.toUpperCase()} ${f.resolution}</a></li>`
                        )
                        .join("");

                    resultBox.innerHTML = `
                        <h3>${data.title}</h3>
                        <p>Uploader: ${data.uploader}</p>
                        <img src="${data.thumbnail}" width="300" style="margin: 10px 0;" />
                        <ul>${formats}</ul>
                    `;
                }
            })
            .catch((err) => {
                resultBox.innerHTML = `<p style="color:red;">Request failed: ${err.message}</p>`;
            });
    });
});
