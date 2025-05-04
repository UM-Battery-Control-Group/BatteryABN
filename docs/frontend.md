# React Frontend Folder Structure

This document provides an overview of the folder structure for the React frontend codebase located in the `frontend/src` folder. If you want to use the frontend dashboard. Start backend flask (for load processed data and images) and flask-rq (for process cell or parse raw data tasks) first.

## Folder Structure

frontend/ │ 
    └── src/ 
        ├── components/ 
        ├── pages/ 
        ├── services/ 
        ├── App.js 
        └── index.js
    └── public


### 1. **components/**

The `components` folder contains reusable UI components that are used across multiple pages in the application.

Example components:
- `Header.js`
- `Footer.js`
- `Button.js`
- `InputField.js`

### 2. **pages/**

The `pages` folder contains all the main views of the application, each representing a unique route in the app.

Example pages:
- `CellDetails.js`
- `CellList.js`
- ...

### 3. **services/**

The `services` folder handles communication with the backend API and manages data fetching and posting. Currently all put in `api.js`


### 4. **App.js**

The `App.js` file is the main entry point of the React application. It contains the routing setup and global components used throughout the app.

### 5. **index.js**

The `index.js` file is where React renders the root component (`App.js`) into the DOM.

---

This structure helps organize the frontend code into clear, modular sections for better maintainability and scalability.
