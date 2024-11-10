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

// Route for the Result Page (result.html)
app.get('/result', (req, res) => {
    res.sendFile(path.join(__dirname, 'result.html'));
});

// Route for the API Page (api.html)
app.get('/api', (req, res) => {
    res.sendFile(path.join(__dirname, 'api.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
