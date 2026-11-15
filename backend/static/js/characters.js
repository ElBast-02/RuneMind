const characterForm = document.getElementById("character-form");
const characterMessage = document.getElementById("character-message");

// ==========================================
// SAVE CHARACTER
// ==========================================

characterForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const characterData = {
        name: document.getElementById("name").value.trim(),
        vigor: Number(document.getElementById("vigor").value),
        strength: Number(document.getElementById("strength").value),
        dexterity: Number(document.getElementById("dexterity").value)
    };

    try {
        const response = await fetch("/api/characters", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(characterData)
        });

        const result = await response.json();

        if (response.ok) {
            characterMessage.textContent = result.message;
            characterForm.reset();

            // Refresh the saved characters immediately
            await loadCharacters();
        } else {
            characterMessage.textContent =
                result.error || "Failed to save character.";
        }

    } catch (error) {
        characterMessage.textContent =
            "Could not connect to the server.";
    }
});


// ==========================================
// LOAD SAVED CHARACTERS
// ==========================================

async function loadCharacters() {
    const characterList = document.getElementById("character-list");

    try {
        const response = await fetch("/api/characters");
        const result = await response.json();

        if (!response.ok) {
            characterList.textContent =
                result.error || "Failed to load characters.";
            return;
        }

        characterList.replaceChildren();

        if (result.characters.length === 0) {
            const message = document.createElement("p");
            message.textContent = "You have no saved characters yet.";
            characterList.appendChild(message);
            return;
        }

        result.characters.forEach(function (character) {
            const card = document.createElement("div");
            card.className = "rm-panel";
            card.style.marginTop = "15px";

            const name = document.createElement("h3");
            name.textContent = character.name;

            const attributes = document.createElement("p");
            attributes.textContent =
                `Vigor: ${character.vigor} | ` +
                `Strength: ${character.strength} | ` +
                `Dexterity: ${character.dexterity}`;

            card.appendChild(name);
            card.appendChild(attributes);
            characterList.appendChild(card);
        });

    } catch (error) {
        characterList.textContent =
            "Could not load saved characters.";
    }
}


// ==========================================
// LOAD CHARACTERS WHEN PAGE OPENS
// ==========================================

loadCharacters();