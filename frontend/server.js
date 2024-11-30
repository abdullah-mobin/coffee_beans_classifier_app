const express = require('express');
const path = require('path');

const app = express();
const port = 3000;

// Serve the static files (CSS, JS, images, etc.) from the 'frontend' directory
app.use(express.static(path.join(__dirname, 'frontend')));

// Route for the Home Page (index.html)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route for the About Page (about.html)
app.get('/about', (req, res) => {
    res.sendFile(path.join(__dirname, 'about.html'));
});

// Route for the Models Page (models.html)
app.get('/models', (req, res) => {
    res.sendFile(path.join(__dirname, 'models.html'));
});

app.get('/history', (req, res) => {
    res.sendFile(path.join(__dirname, 'history.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://192.168.1.102:${port}`);
});
