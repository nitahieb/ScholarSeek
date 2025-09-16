# React Frontend for PubMed Author Finder

This directory contains the React frontend for the PubMed Author Finder application.

## Features

- Modern React application with TypeScript
- Responsive UI design matching the original Flask template
- Real-time search with loading states
- Error handling and user feedback
- Markdown rendering for search results
- Table rendering for structured data

## Development

To run the React development server:

```bash
cd frontend
npm install
npm start
```

The development server will start on http://localhost:3000 and proxy API requests to the Flask backend (should be running on http://localhost:5000).

## Production Build

To create a production build:

```bash
cd frontend
npm run build
```

The Flask application is configured to serve the built React app from the `frontend/build` directory.

## API Integration

The React app communicates with the Flask backend via the following endpoints:

- `GET /api/health` - Health check
- `POST /api/search` - Search PubMed articles

## Components

- `PubMedSearch` - Main search interface component
- `SearchForm` - Search form with validation
- `SearchResults` - Display search results with markdown rendering
- `ErrorDisplay` - Error message display component

## Running the Complete Application

Use the provided script to build and run the complete application:

```bash
./run_react_app.sh
```

This will:
1. Install React dependencies
2. Build the React frontend
3. Start the Flask server serving the React app

---

## Original Create React App Documentation

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
