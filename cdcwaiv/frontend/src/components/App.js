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
import {render} from 'react-dom';
import { createRoot } from 'react-dom/client'; 
import HomePage from './HomePage';
import StudentPage from './Student';
import MonthlyListing from './MonthlyListing'
import Employee from './Employee';
import Profile from './Profile';

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <div>
            <HomePage />
            <Employee />
            <StudentPage />
            <MonthlyListing />
            <Profile />
        </div>
        );
    }
}

const appDiv = document.getElementById("app");
const root = createRoot(appDiv); 
root.render(<App />); 
