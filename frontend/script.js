document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("predictBtn");
    btn.addEventListener("click", async () => {
        const inputStr = document.getElementById("features").value.trim();
        const features = inputStr.split(",").map(num => parseFloat(num));

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ features: features })
            });

            const result = await response.json();
            document.getElementById("result").innerText = `Prediction: ${result.prediction}`;
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("result").innerText = "Error in prediction!";
        }
    });
});
