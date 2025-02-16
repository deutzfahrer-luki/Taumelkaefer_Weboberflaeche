function initializeJoystick(joystickElement, containerElement, outputElement) {
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

        outputElement.textContent = `X: ${xValue}, Y: ${yValue}`;
    }

    // Setzt den Joystick in die Mitte zurück
    function resetJoystick() {
        joystickElement.style.transform = 'translate(0, 0)';
        outputElement.textContent = 'X: 0, Y: 0';
    }

    // Touch Move (für Touchscreen)
    function handleTouchMove(e) {
        Array.from(e.touches).forEach(touch => {
            if (touches[touch.identifier]) {
                const touchData = touches[touch.identifier];
                const x = touch.clientX - containerRect.left - centerX;
                const y = touch.clientY - containerRect.top - centerY;
                handleMove(x, y);
            }
        });
    }

    // Maus Move (für Laptop)
    function handleMouseMove(e) {
        if (isDragging) {
            const x = e.clientX - containerRect.left - centerX;
            const y = e.clientY - containerRect.top - centerY;
            handleMove(x, y);
        }
    }

    // Touch Start
    joystickElement.addEventListener('touchstart', (e) => {
        Array.from(e.touches).forEach(touch => {
            touches[touch.identifier] = true;
            const x = touch.clientX - containerRect.left - centerX;
            const y = touch.clientY - containerRect.top - centerY;
            handleMove(x, y);
        });
    });

    // Mouse Down
    joystickElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        const x = e.clientX - containerRect.left - centerX;
        const y = e.clientY - containerRect.top - centerY;
        handleMove(x, y);
    });

    // Global Touch Move und Mouse Move
    window.addEventListener('touchmove', handleTouchMove);
    window.addEventListener('mousemove', handleMouseMove);

    // Touch End
    window.addEventListener('touchend', (e) => {
        Array.from(e.changedTouches).forEach(touch => {
            delete touches[touch.identifier];
            if (Object.keys(touches).length === 0) {
                resetJoystick();
            }
        });
    });

    // Mouse Up
    window.addEventListener('mouseup', () => {
        isDragging = false;
        resetJoystick();
    });
}

// Initialisierung der Joysticks
const joystickLeft = document.getElementById('joystick-left');
const containerLeft = document.getElementById('joystick-container-left');
const outputLeft = document.getElementById('output-left');
initializeJoystick(joystickLeft, containerLeft, outputLeft);

const joystickRight = document.getElementById('joystick-right');
const containerRight = document.getElementById('joystick-container-right');
const outputRight = document.getElementById('output-right');
initializeJoystick(joystickRight, containerRight, outputRight);