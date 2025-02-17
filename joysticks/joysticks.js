// Funktion zum Initialisieren des Joysticks
function initializeJoystick(joystickElement, containerElement, onJoystickMoveCallback) {
    const containerRect = containerElement.getBoundingClientRect();
    const centerX = containerRect.width / 2;
    const centerY = containerRect.height / 2;
    const maxDistance = 75;

    let touches = {};  // Track multiple touches for each joystick
    let isDragging = false;  // Track if we are dragging with the mouse

    // Bewege den Joystick
    function handleMove(x, y) {
        const distance = Math.sqrt(x * x + y * y);
        if (distance > maxDistance) {
            x = (x / distance) * maxDistance;
            y = (y / distance) * maxDistance;
        }

        joystickElement.style.transform = `translate(${x}px, ${y}px)`;

        const xValue = Math.round((x / maxDistance) * 255);
        const yValue = Math.round((y / maxDistance) * 255);

        return [xValue, yValue]; // Return the joystick values as an array
    }

    // Setzt den Joystick in die Mitte zurück
    function resetJoystick() {
        joystickElement.style.transform = 'translate(0, 0)';
        return [0, 0]; // Return neutral position
    }

    // Touch Move (für Touchscreen)
    function handleTouchMove(e) {
        Array.from(e.touches).forEach(touch => {
            if (touches[touch.identifier]) {
                const x = touch.clientX - containerRect.left - centerX;
                const y = touch.clientY - containerRect.top - centerY;
                const values = handleMove(x, y);
                onJoystickMoveCallback(values); // Callback für die Werte
            }
        });
    }

    // Maus Move (für Laptop)
    function handleMouseMove(e) {
        if (isDragging) {
            const x = e.clientX - containerRect.left - centerX;
            const y = e.clientY - containerRect.top - centerY;
            const values = handleMove(x, y);
            onJoystickMoveCallback(values); // Callback für die Werte
        }
    }

    // Touch Start
    joystickElement.addEventListener('touchstart', (e) => {
        Array.from(e.touches).forEach(touch => {
            touches[touch.identifier] = true;
            const x = touch.clientX - containerRect.left - centerX;
            const y = touch.clientY - containerRect.top - centerY;
            const values = handleMove(x, y);
            onJoystickMoveCallback(values); // Callback für die Werte
        });
    });

    // Mouse Down
    joystickElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        const x = e.clientX - containerRect.left - centerX;
        const y = e.clientY - containerRect.top - centerY;
        const values = handleMove(x, y);
        onJoystickMoveCallback(values); // Callback für die Werte
    });

    // Global Touch Move und Mouse Move
    window.addEventListener('touchmove', handleTouchMove);
    window.addEventListener('mousemove', handleMouseMove);

    // Touch End
    window.addEventListener('touchend', (e) => {
        Array.from(e.changedTouches).forEach(touch => {
            delete touches[touch.identifier];
            if (Object.keys(touches).length === 0) {
                const values = resetJoystick();
                onJoystickMoveCallback(values); // Callback für die Werte
            }
        });
    });

    // Mouse Up
    window.addEventListener('mouseup', () => {
        isDragging = false;
        const values = resetJoystick();
        onJoystickMoveCallback(values); // Callback für die Werte
    });
}


// Funktion zum Aktualisieren des Outputs und der Konsole
function updateOutput(values, outputElement, index) {
    outputElement.textContent = `X: ${values[0]}, Y: ${values[1]}`;
    console.log(`${index}:`, values); // Korrigierte Konsolenausgabe
}

// Initialisierung der Joysticks
const joystickLeft = document.getElementById('joystick-left');
const containerLeft = document.getElementById('joystick-container-left');
const outputLeft = document.getElementById('output-left');

const joystickRight = document.getElementById('joystick-right');
const containerRight = document.getElementById('joystick-container-right');
const outputRight = document.getElementById('output-right');

// Callback-Funktionen für die Joysticks
function onJoystickMoveLeft(values) {
    updateOutput(values, outputLeft, "left"); // Update left joystick output
}

function onJoystickMoveRight(values) {
    updateOutput(values, outputRight, "right"); // Update right joystick output
}

// Joysticks initialisieren
initializeJoystick(joystickLeft, containerLeft, onJoystickMoveLeft);
initializeJoystick(joystickRight, containerRight, onJoystickMoveRight);