// import React, { Component } from 'react';
// import { render } from 'react-dom';

// export default class App extends Component {
//     constructor(props) {
//         super(props);
//     }

//     render() {
//         return <h1>Welcome to the WAIV App</h1>;
//     }
// }

// const appDiv = document.getElementById("app");
// render(<App />, appDiv);
import React, { Component } from 'react';
import { createRoot } from 'react-dom/client'; 

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <h1>Welcome to the WAIV App</h1>;
    }
}

// Mount React to Django's <div id="app"></div>
const appDiv = document.getElementById("app");
const root = createRoot(appDiv); // ⚡ createRoot instead of render
root.render(<App />); // ⚡ use root.render
